from collections import defaultdict
from collections.abc import Iterable
from functools import singledispatch
from itertools import islice

from asm68.addrmodes import (
    PageDirect,
    ExtendedDirect,
    Inherent,
    Immediate,
    Indexed,
    Integers,
    Registers)
from asm68.util import single
from asm68.directives import Org, Fcb, Fdb, Call
from asm68.instructions import Instruction
from asm68.label import Label
from asm68.opcodes import OPCODES, Integral
from asm68.registers import X, Y, U, S, A, B, D, E, F, V, W, Z, AutoIncrementedRegister, PC, CC, DP
from asm68.twiddle import twos_complement, hi, lo
from asm68.asmdsl import PROGRAM_COUNTER_LABEL_NAME


def assemble(statements, *, origin=0, logger=None):
    """
    Args:
        statements: The sequence of statements to be assembled.
        origin: The start address for assembly.
        warnings: An optional mutable sequence to which warning messages will be appended.
    """
    asm = Assembler(origin, logger=logger)
    asm.assemble(statements, origin)
    code = asm.object_code()
    return code


class TooManyPassesError(Exception):

    def __init__(self, num_passes, unresolved_labels, unreferenced_labels):
        self.num_passes = num_passes
        self.unresolved_labels = unresolved_labels
        self.unreferenced_labels = unreferenced_labels
        super().__init__(
            f"Too many passes ({self.num_passes})"
        )

    @property
    def unresolved_label_names(self):
        return sorted(label.name for label in self.unresolved_labels)

    @property
    def unreferenced_label_names(self):
        return sorted(self.unreferenced_labels)


class InterRegisterError(Exception):

    def __init__(self, message, register):
        super().__init__(message)
        self._register = register

    @property
    def register(self):
        return self._register



class Assembler:

    def __init__(self, origin=0, logger=None):
        self._origin = origin
        self._pos = self.origin
        self._code = defaultdict(list)  # A dictionary mapping addresses to code fragments represented as lists of bytes strings.
        self._label_addresses = {}  # Maps label names to items in _code
        self._unreferenced_labels = set()
        self._unresolved_labels = set()
        self._more_passes_required = True
        self._logger = logger
        self._i = 0

    def __str__(self):
        lines = [
            f"Origin: 0x{self.origin:04X}",
            f"PC:     0x{self.pos:04X}",
        ]
        return "\n".join(lines)

    @property
    def pos(self):
        return self._pos

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        # If the origin falls within an existing fragment, reject the change
        self._flatten()
        if self._in_existing_fragment(value):
            raise ValueError("Origin address 0x{:04X} lies within existing code fragment".format(value))
        self._origin = value
        self._pos = self._origin

    @property
    def unresolved_labels(self):
        """A set of unresolved labels.
        """
        return self._unreferenced_labels

    @property
    def unreferenced_labels(self):
        """A set of unreferenced labels.
        """
        return self._unreferenced_labels

    @property
    def label_addresses(self):
        """A mapping from label names to label addresses.
        """
        return self._label_addresses

    def _in_existing_fragment(self, value):

        return any(value in range(address, len(code[0])) for address, code in self._code.items())

    def _flatten(self):
        self._code = defaultdict(
            list,
            ((address, [b''.join(fragments)])
             for address, fragments in self._code.items()))

    def _extend(self, code):
        # TODO: Check that we're not extending into an existing fragment - use interval tree for this
        c = bytes(code)
        self._code[self.origin].append(c)
        self._pos += len(c)

    def object_code(self):
        self._flatten()
        return {address: fragments[0] for address, fragments in self._code.items()}

    def assemble(self, statements, origin=0, max_passes=3):
        # Do multi-pass assembly
        self._i = 0
        while self._more_passes_required:
            self._more_passes_required = False
            self._code.clear()
            self.origin = origin
            for statement in statements:
                self.assemble_statement(statement)
            self._i += 1
            if self._i > max_passes:
                raise TooManyPassesError(
                    num_passes=self._i,
                    unresolved_labels=self._unresolved_labels,
                    unreferenced_labels=self._unreferenced_labels
                )
        self._warn_about_unreferenced_labels()

    def _warn_about_unreferenced_labels(self):
        if self._logger:
            for label in self.unreferenced_labels:
                self._logger.warning("Unreferenced label: %s", label)

    def assemble_statement(self, statement):
        self._label_addresses[PROGRAM_COUNTER_LABEL_NAME] = self.pos
        self._label_statement(statement)
        assemble_statement(statement, self)

    def _label_statement(self, statement):
        label = statement.label
        while label is not None:
            if label.name in self._label_addresses:
                if self._label_addresses[label.name] != self.pos:
                    # Different address used. What we do here depends on
                    # which compiler pass this is.
                    if self._i == 0:
                        raise RuntimeError("Label {} already used previously."
                                           .format(label))
                    # else:
                    #    print("More passes required.")
            self._label_addresses[label.name] = self.pos
            self._unreferenced_labels.add(label.name)
            self._unresolved_labels.discard(label.name)
            label = label.chained_label

    def assemble_operand(self, operand, opcode_key, statement, opcode_bytes):
        return assemble_operand(operand, opcode_key, self, statement, opcode_bytes)

    def assemble_inherent_operand(self, operand, opcode_key, statement, opcode_bytes):
        return bytes()

    def assemble_immediate_operand(self, operand, opcode_key, statement, opcode_bytes):
        if isinstance(operand, Label):
            result = self.assemble_label_operand(operand)
        else:
            assert statement.inherent_register.width in {1, 2}
            if statement.inherent_register.width == 1:
                result = (operand.value, )
            elif statement.inherent_register.width == 2:
                result = (hi(operand.value), lo(operand.value))
            else:
                assert False, f"Unexpected inherent register width {statement.inherent_register.width}"
        return bytes(result)

    def assemble_page_direct_operand(self, operand, opcode_key, statement, opcode_bytes):
        # TODO: What about labels?
        return bytes((operand.address, ))

    def assemble_extended_direct_operand(self, operand, opcode_key, statement, opcode_bytes):
        if isinstance(operand.address, Label):
            result = self.assemble_label_operand(operand.address)
        else:
            result = (hi(operand.address), lo(operand.address))
        return bytes(result)

    def assemble_indexed_operand(self, operand: Indexed, opcode_key, statement, opcode_bytes):
        if operand.base in RR:
            rr = RR[operand.base]
            if operand.offset in ACCUMULATOR_OFFSET_POST_BYTE:
                # Accumulator offset
                post_byte = ACCUMULATOR_OFFSET_POST_BYTE[operand.offset]
                post_byte |= rr << 5
                return bytes((post_byte, ))
            elif isinstance(operand.offset, Integral):
                if operand.offset == 0:
                    post_byte = 0b10000100
                    post_byte |= rr << 5
                    return bytes((post_byte, ))
                elif -16 <= operand.offset <= +15:
                    # 5-bit offset
                    post_byte = twos_complement(operand.offset, 5)
                    post_byte |= rr << 5
                    return bytes((post_byte, ))
                elif -128 <= operand.offset <= +127:
                    # 8-bit offset
                    post_byte = 0b10001000
                    post_byte |= rr << 5
                    offset_byte = twos_complement(operand.offset, 8)
                    return bytes((post_byte, offset_byte))
                elif -32768 <= operand.offset <= +32767:
                    # 16-bit offset
                    post_byte = 0b10001001
                    post_byte |= rr << 5
                    offset_bytes = twos_complement(operand.offset, 16)
                    return bytes((post_byte, hi(offset_bytes), lo(offset_bytes)))
            else:
                raise ValueError(f"Cannot use indexed addressing offset {operand.offset} with base {operand.base}")

        elif isinstance(operand.base, AutoIncrementedRegister):
            if operand.base.register not in RR:
                raise ValueError(f"Cannot use auto pre-/post- increment or decrement with register {operand.base.register}")
            rr = RR[operand.base.register]
            post_byte = INDEX_CREMENT_POST_BYTE[operand.base.delta]
            post_byte |= rr << 5
            return bytes((post_byte, ))
        else:
            raise ValueError(f"Cannot use {operand.base} as a base register for indexed addressing modes")

    def assemble_short_relative_operand(self, operand, opcode_key, statement, opcode_bytes):
        return self._assemble_relative_operand(operand, operand_bytes_length=1, opcode_bytes=opcode_bytes)

    def assemble_long_relative_operand(self, operand, opcode_key, statement, opcode_bytes):
        return self._assemble_relative_operand(operand, operand_bytes_length=2, opcode_bytes=opcode_bytes)

    def _assemble_relative_operand(self, operand, operand_bytes_length, opcode_bytes):
        if isinstance(operand.address, Label):
            if operand.name in self._label_addresses:
                target_address = self._label_addresses[operand.name]
                # TODO: Consider threading opcode_bytes through as an argument
                offset = target_address - self.pos - len(opcode_bytes) - operand_bytes_length
                unsigned_offset = twos_complement(offset, operand_bytes_length * 8)
                result = self.value_to_bytes(unsigned_offset, operand_bytes_length)
                self._unresolved_labels.discard(operand.name)
            else:
                self._more_passes_required = True
                result = bytes(operand_bytes_length)
                self._unresolved_labels.add(operand.name)
            self._unreferenced_labels.discard(operand.name)
        else:
            # TODO: What if the operand is a number?
            raise NotImplementedError
        return result

    def value_to_bytes(self, unsigned_offset, operand_bytes_length):
        if operand_bytes_length == 1:
            result = bytes((unsigned_offset,))
        elif operand_bytes_length == 2:
            result = bytes((hi(unsigned_offset), lo(unsigned_offset)))
        else:
            assert False, f"Unexpected operand bytes length {operand_bytes_length}"
        return result

    def assemble_register_operand(self, operand, opcode_key, statement, opcode_bytes):
        assert isinstance(operand, Registers)
        source, target = operand.registers
        try:
            source_nybble = REGISTER_NYBBLES[source]
        except KeyError:
            raise InterRegisterError(f"Cannot use {source} as source register for inter-register instructions", source)
        try:
            target_nybble = REGISTER_NYBBLES[target]
        except KeyError:
            raise InterRegisterError(f"Cannot use {target} as target register for inter-register instructions", target)
        result = (source_nybble << 4) | target_nybble
        return bytes((result,))

    def assemble_label_operand(self, label):
        if label.name in self._label_addresses:
            target_address = self._label_addresses[label.name]
            self._unresolved_labels.discard(label.name)
            result = (hi(target_address), lo(target_address))
        else:
            self._more_passes_required = True
            self._unresolved_labels.add(label.name)
            result = (0, 0)
        self._unreferenced_labels.discard(label.name)
        return result

@singledispatch
def assemble_statement(statement, asm):
    raise TypeError("Statement {} could not be assembled".format(statement))

@assemble_statement.register(Instruction)
def _(statement, asm):
    operand = statement.operand

    operating_addressing_modes = set(operand.codes)

    opcodes = OPCODES[statement.mnemonic.key]
    opcode_key = single(operating_addressing_modes & opcodes.keys())
    opcode_bytes = bytes.fromhex(opcodes[opcode_key])
    # TODO: Dispatch this back to a method on the instruction
    #       Maybe assemble_with_operand instead of assembling
    #       the opcode separately here
    operand_bytes = statement.assemble_operand(operand, opcode_key, asm, opcode_bytes)
    asm._extend(opcode_bytes + operand_bytes)


@assemble_statement.register(Org)
def _(statement, asm):
    operand = statement.operand
    if not isinstance(operand, Immediate):
        raise TypeError("ORG operand must be an immediate value")
    asm.origin = operand.value


@assemble_statement.register(Fcb)
def _(statement, asm):
    operand = statement.operand
    if not isinstance(operand, Integers):
        raise TypeError("FCB value must be integers")
    try:
        b = bytes(operand)
    except ValueError as e:
        g = ((i, v) for i, v in enumerate(operand) if not v in range(0, 256))
        i, v = next(islice(g, 1))
        raise ValueError("FCB value {} at index {} not in range(0, 256)".format(v, i)) from e
    asm._extend(b)


@assemble_statement.register(Fdb)
def _(statement, asm):
    operand = statement.operand
    if not isinstance(operand, Integers):
        raise TypeError("FDB value must be integers")
    b = bytearray()
    for i, v in enumerate(operand):
        hi, lo = fdb_value(v, asm)
        b.append(hi)
        b.append(lo)
    asm._extend(b)


def fdb_value(v, asm):
    if isinstance(v, Label):
        if v.name in asm._label_addresses:
            value = asm._label_addresses[v.name]
            asm._unresolved_labels.discard(v.name)
        else:
            value = 0
            asm._more_passes_required = True
            asm._unresolved_labels.add(v.name)
        asm._unreferenced_labels.discard(v.name)
    else:
        value = v
    if value not in range(0, 65536):
        raise ValueError(f"FDB value {value} (0x{value:04x}) not in 0–65535 (0x0000-0xFFFF)")
    hi = (value >> 8) & 0xff
    lo = value & 0xff
    return hi, lo


@assemble_statement.register(Call)
def _(statement, asm):
    """Invoke an assembler macro for expansion inline.

    The operand of the call directive must be a a Python callable to which
    the assember instance will be passed. The macro function can return an
    iterable series of statements, in which case they will be assembled,
    a single statement to be assembled. Macros which return None can be useful
    for the side-effects. For example, the built-in function 'print' can be
    CALLed to print the current assembler state.
    """
    operand = statement.operand
    if not callable(operand):
        raise TypeError("CALL value must be a Python callable")
    result = operand(asm)
    if isinstance(result, Iterable):
        for stmt in result:
            assemble_statement(stmt, asm)


class TypeMismatchError(Exception):
    pass


@singledispatch
def assemble_operand(operand, opcode_key, asm, statement, opcode_bytes):
    raise TypeError("Operand {} could not be assembled".format(operand))


@assemble_operand.register(Inherent)
def _(operand, opcode_key, asm, statement, opcode_bytes):
    try:
        operand_assembler = statement.inherent_operand
    except AttributeError:
        raise TypeMismatchError(f"statement {statement.mnemonic} does not support inherent addressing")
    return operand_assembler(operand, opcode_key, asm, opcode_bytes)


@assemble_operand.register(Immediate)
def _(operand, opcode_key, asm, statement, opcode_bytes):
    try:
        operand_assembler = statement.immediate_operand
    except AttributeError:
        raise TypeMismatchError(f"statement {statement.mnemonic} does not support immediate operands")
    return operand_assembler(operand, opcode_key, asm, opcode_bytes)


@assemble_operand.register(PageDirect)
def _(operand, opcode_key, asm, statement, opcode_bytes):
    try:
        operand_assembler = statement.page_direct_operand
    except AttributeError:
        raise TypeMismatchError(f"statement {statement.mnemonic} does not support page-direct operands")
    return operand_assembler(operand, opcode_key, asm, opcode_bytes)


@assemble_operand.register(ExtendedDirect)
def _(operand, opcode_key, asm, statement, opcode_bytes):
    try:
        operand_assembler = statement.extended_direct_operand
    except AttributeError:
        raise TypeMismatchError(f"statement {statement.mnemonic} does not support extended direct operands")
    return operand_assembler(operand, opcode_key, asm, opcode_bytes)


@assemble_operand.register(Label)
def _(operand, opcode_key, asm, statement, opcode_bytes):
    try:
        operand_assembler = statement.relative_operand
    except AttributeError:
        try:
            operand_assembler = statement.immediate_operand
        except AttributeError:
            raise TypeMismatchError(f"statement {statement.mnemonic} does not support label operands")
    return operand_assembler(operand, opcode_key, asm, opcode_bytes)


RR = {X: 0b00,
      Y: 0b01,
      U: 0b10,
      S: 0b11}

ACCUMULATOR_OFFSET_POST_BYTE = {
    A: 0b10000110,
    B: 0b10000101,
    D: 0b10001011,
    E: 0b10000111,
    F: 0b10001010,
    W: 0b10001110
}

INDEX_CREMENT_POST_BYTE = {
    +1: 0b10000000,
    +2: 0b10000001,
    -1: 0b10000010,
    -2: 0b10000011,
}

@assemble_operand.register(Indexed)
def _(operand, opcode_key, asm, statement, opcode_bytes):
    try:
        operand_assembler = statement.indexed_operand
    except AttributeError:
        raise TypeMismatchError(f"statement {statement.mnemonic} does not support indexed operands")
    return operand_assembler(operand, opcode_key, asm, opcode_bytes)


REGISTER_NYBBLES_6809 = {
    D: 0b0000,
    X: 0b0001,
    Y: 0b0010,
    U: 0b0011,
    S: 0b0100,
    PC: 0b0101,
    A: 0b1000,
    B: 0b1001,
    CC: 0b1010,
    DP: 0b1011,
}

REGISTER_NYBBLES_6309 = {
    W: 0b0110,
    V: 0b0111,
    Z: 0b1100,
    E: 0b1110,
    F: 0b1111,
}

REGISTER_NYBBLES = {**REGISTER_NYBBLES_6809, **REGISTER_NYBBLES_6309}


@assemble_operand.register(Registers)
def _(operand, opcode_key, asm, statement, opcode_bytes):
    return statement.register_operand(operand, opcode_key, asm, opcode_bytes)
