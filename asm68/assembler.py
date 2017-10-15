from functools import singledispatch

from asm68.addrmodecodes import REL8, REL16
from asm68.addrmodes import PageDirect, Inherent, Immediate
from asm68.asmdsl import single
from asm68.label import Label
from asm68.opcodes import OPCODES

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
        # Do two-pass assembly
        for i in range(2):
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
                self._extend(self._opcode_bytes + assemble_operand(operand, opcode_key, self))

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
def assemble_operand(operand, opcode_key, asm):
    raise NotImplementedError("Operand {} could not be assembled".format(operand))

@assemble_operand.register(Inherent)
def _(operand, opcode_key, asm):
    return ()

@assemble_operand.register(Immediate)
def _(operand, opcode_key, asm):
    return (operand.value, )

@assemble_operand.register(PageDirect)
def _(operand, opcode_key, asm):
    return (operand.address, )

@assemble_operand.register(Label)
def _(operand, opcode_key, asm):
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

    return (unsigned_offset, )


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
