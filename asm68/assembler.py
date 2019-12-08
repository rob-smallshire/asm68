from collections import defaultdict
from functools import singledispatch
from itertools import islice

from asm68.addrmodecodes import REL8, REL16, IMM
from asm68.addrmodes import (PageDirect, Inherent, Immediate, Indexed, Integers)
from asm68.util import single
from asm68.directives import Org, Fcb, Fdb
from asm68.instructions import Instruction
from asm68.label import Label
from asm68.opcodes import OPCODES, Integral
from asm68.registers import X, Y, U, S, A, B, D, E, F, W, AutoIncrementedRegister
from asm68.twiddle import twos_complement, hi, lo


def assemble(statements, origin=0):
    asm = Assembler(origin)
    asm.assemble(statements)
    return asm.object_code()


class Assembler:

    def __init__(self, origin=0):
        self._origin = origin
        self._pos = self.origin
        self._code = defaultdict(list)  # A dictionary mapping addresses to code fragments represented as lists of bytes strings.
        self._label_addresses = {}  # Maps label names to items in _code
        self._more_passes_required = True

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

    def assemble(self, statements):
        # Do multi-pass assembly
        i = 0
        while self._more_passes_required:
            self._more_passes_required = False
            self._code.clear()
            self.origin = 0
            for statement in statements:
                self._label_statement(statement, i)
                assemble_statement(statement, self)
            i += 1

    def _label_statement(self, statement, i):
        if statement.label is not None:
            if statement.label in self._label_addresses:
                if self._label_addresses[statement.label] != self._pos:
                    # Different address used. What we do here depends on
                    # which compiler pass this is.
                    if i == 0:
                        raise RuntimeError("Label {} already used previously."
                                           .format(statement.label))
                    # else:
                    #    print("More passes required.")
            self._label_addresses[statement.label] = self._pos

@singledispatch
def assemble_statement(statement, asm):
    raise TypeError("Statement {} could not be assembled".format(statement))

@assemble_statement.register(Instruction)
def _(statement, asm):
    operand = statement.operand
    opcodes = OPCODES[statement.mnemonic]
    opcode_key = single(operand.codes & opcodes.keys())
    opcode = opcodes[opcode_key]
    asm._opcode_bytes = (opcode,) if opcode <= 0xFF else (hi(opcode), lo(opcode))
    operand_bytes = assemble_operand(operand, opcode_key, asm, statement)
    asm._extend(asm._opcode_bytes + operand_bytes)

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
        if v not in range(0, 65536):
            raise ValueError("FDB value {} at index {} not in range(0, 65536)")
        b.append((v >> 8) & 0xff)
        b.append(v & 0xff)
    asm._extend(b)

@singledispatch
def assemble_operand(operand, opcode_key, asm, statement):
    raise TypeError("Operand {} could not be assembled".format(operand))

@assemble_operand.register(Inherent)
def _(operand, opcode_key, asm, statement):
    return ()

@assemble_operand.register(Immediate)
def _(operand, opcode_key, asm, statement):
    assert statement.inherent_register.width in {1, 2}
    if statement.inherent_register.width == 1:
        return (operand.value, )
    elif statement.inherent_register.width == 2:
        return (hi(operand.value), lo(operand.value))

@assemble_operand.register(PageDirect)
def _(operand, opcode_key, asm, statement):
    return (operand.address, )

branch_operand_widths = {
    REL8: 1,
    REL16: 2
}

@assemble_operand.register(Label)
def _(operand, opcode_key, asm, statement):
    # If we know the address of the label, use it
    if operand.name in asm._label_addresses:
        target_address = asm._label_addresses[operand.name]
        if opcode_key in branch_operand_widths:
            operand_bytes_length = branch_operand_widths[opcode_key]
            offset = target_address - asm.pos - len(asm._opcode_bytes) - operand_bytes_length
            unsigned_offset = twos_complement(offset, operand_bytes_length * 8)
            if opcode_key == REL8:
                return (unsigned_offset, )
            elif opcode_key == REL16:
                return (hi(unsigned_offset), lo(unsigned_offset))
        else:
            assert opcode_key is IMM
            return (hi(target_address), lo(target_address))
    else:
        asm._more_passes_required = True
        if opcode_key in branch_operand_widths:
            return (0, ) * branch_operand_widths[opcode_key]
        else:
            assert opcode_key is IMM
            return (0, 0)



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
def _(operand, opcode_key, asm, statement):
    if operand.base in RR:
        rr = RR[operand.base]
        if operand.offset in ACCUMULATOR_OFFSET_POST_BYTE:
            # Accumulator offset
            post_byte = ACCUMULATOR_OFFSET_POST_BYTE[operand.offset]
            post_byte |= rr << 5
            return (post_byte, )
        elif isinstance(operand.offset, Integral):
            if operand.offset == 0:
                post_byte = 0b10000100
                post_byte |= rr << 5
                return (post_byte, )
            elif -16 <= operand.offset <= +15:
                # 5-bit offset
                post_byte = twos_complement(operand.offset, 5)
                post_byte |= rr << 5
                return (post_byte, )
            elif -128 <= operand.offset <= +127:
                # 8-bit offset
                post_byte = 0b10001000
                post_byte |= rr << 5
                offset_byte = twos_complement(operand.offset, 8)
                return (post_byte, offset_byte)
            elif -32768 <= operand.offset <= +32767:
                # 16-bit offset
                post_byte = 0b10001001
                post_byte |= rr << 5
                offset_bytes = twos_complement(operand.offset, 16)
                return (post_byte, hi(offset_bytes), lo(offset_bytes))
        else:
            raise ValueError(f"Cannot use indexed addressing offset {operand.offset} with base {operand.base}")

    elif isinstance(operand.base, AutoIncrementedRegister):
        if operand.base.register not in RR:
            raise ValueError(f"Cannot use auto pre-/post- increment or decrement with register {operand.base.register}")
        rr = RR[operand.base.register]
        post_byte = INDEX_CREMENT_POST_BYTE[operand.base.delta]
        post_byte |= rr << 5
        return (post_byte, )
    else:
        raise ValueError(f"Cannot use {operand.base} as a base register for indexed addressing modes")


