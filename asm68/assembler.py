from functools import singledispatch

from asm68.addrmodecodes import REL8, REL16
from asm68.addrmodes import (PageDirect, Inherent, Immediate, Registers, Indexed)
from asm68.asmdsl import single
from asm68.label import Label
from asm68.opcodes import OPCODES
from asm68.registers import X, Y, U, S, A, B, D, E, F, W


def assemble(statements, origin=None):
    asm = Assembler(origin)
    asm.assemble(statements)
    return asm.object_code()

class Assembler:

    def __init__(self, origin=None):
        if origin is None:
            origin = 0
        self._origin = origin
        self._pos = self._origin
        # TODO: Store addresses and code separately, so the code can be cleared.
        self._code = []  # A list of (bytes) pairs, one item per statement. (address, code)
        self._label_addresses = {}  # Maps label names to items in _code
        self._more_passes_required = True

    @property
    def pos(self):
        return self._pos

    def _extend(self, code):
        c = bytes(code)
        self._code.append(c)
        self._pos += len(c)

    def object_code(self):
        return b''.join(self._code)

    def assemble(self, statements):
        # Do multi-pass assembly
        i = 0
        while self._more_passes_required:
            self._more_passes_required = False
            self._code.clear()
            self._pos = 0
            for statement in statements:
                self._label_statement(statement, i)

                operand = statement.operand

                try:
                    opcodes = OPCODES[statement.mnemonic]
                except KeyError:
                    raise RuntimeError("No opcodes for {}".format(statement.mnemonic))

                try:
                    opcode_key = single(operand.codes & opcodes.keys())
                except ValueError:
                    raise RuntimeError("{} does not support {} addressing modes.".format(statement.mnemonic, operand.codes))

                opcode = opcodes[opcode_key]
                self._opcode_bytes = (opcode, ) if opcode <= 0xFF else (hi(opcode), lo(opcode))
                self._extend(self._opcode_bytes + assemble_operand(operand, opcode_key, self, statement))
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
                    else:
                        print("More passes required.")
            self._label_addresses[statement.label] = self._pos


@singledispatch
def assemble_operand(operand, opcode_key, asm, statement):
    raise NotImplementedError("Operand {} could not be assembled".format(operand))

@assemble_operand.register(Inherent)
def _(operand, opcode_key, asm, statement):
    return ()

@assemble_operand.register(Immediate)
def _(operand, opcode_key, asm, statement):
    if statement.inherent_register.width == 1:
        return (operand.value, )
    elif statement.inherent_register.width == 2:
        return (hi(operand.value), lo(operand.value))
    else:
        assert False, "Unhandled immediate value width of {} bytes".format(
            statement.inherent_register.width)

@assemble_operand.register(PageDirect)
def _(operand, opcode_key, asm, statement):
    return (operand.address, )

@assemble_operand.register(Label)
def _(operand, opcode_key, asm, statement):
    # If we know the address of the label, use it
    if operand.name in asm._label_addresses:
        target_address = asm._label_addresses[operand.name]

        if opcode_key is REL8:
            operand_bytes_length = 1
        # elif opcode_key is REL16:
        #     operand_bytes_length = 2
        else:
            assert False, "Unhandled addressing mode."

        offset = target_address - asm.pos - len(asm._opcode_bytes) - operand_bytes_length
        unsigned_offset = twos_complement(offset, operand_bytes_length * 8)

    else:
        unsigned_offset = 0
        asm._more_passes_required = True

    return (unsigned_offset, )

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

@assemble_operand.register(Indexed)
def _(operand, opcode_key, asm, statement):
    print(operand)
    try:
        rr = RR[operand.base]
    except KeyError:
        raise ValueError("Cannot use {} as a base for indexed addressing.".format(operand.base))
    if operand.offset in ACCUMULATOR_OFFSET_POST_BYTE:
        # Accumulator offset
        post_byte = ACCUMULATOR_OFFSET_POST_BYTE[operand.offset]
        post_byte |= rr << 5
        return (post_byte, )



def twos_complement(n, num_bits):
    lower = -(2**(num_bits - 1))
    higher = 2**(num_bits - 1) - 1
    if not (lower <= n <= higher):
        raise ValueError("Cannot represent {} in two's complement in {} bits".format(n, num_bits))

    if n < 0:
        return n + (1 << num_bits)
    return n

def hi(b):
    return b >> 8

def lo(b):
    return b & 0xFF
