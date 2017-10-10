from functools import singledispatch

from asm68.addrmodes import PageDirect, Inherent, Immediate
from asm68.asmdsl import single
from asm68.opcodes import OPCODES


def assemble(statements):

    code = bytearray()

    for statement in statements:
        #print(statement)
        operand = statement.operand
        #print(operand.codes)

        try:
            opcodes = OPCODES[statement.mnemonic]
        except KeyError:
            raise RuntimeError("No opcodes for {}".format(statement.mnemonic))

        try:
            opcode_key = single(operand.codes & opcodes.keys())
        except ValueError:
            raise RuntimeError("{} does not support {} addressing modes.".format(statement.mnemonic, operand.codes))
        #print(opcode_key)
        opcode = opcodes[opcode_key]
        #print(hex(opcode))

        opcode_bytes = (opcode, ) if opcode <= 0xFF else (hi(opcode), lo(opcode))

        code.extend(opcode_bytes)

        code.extend(assemble_operand(operand))

    return bytes(code)

@singledispatch
def assemble_operand(operand):
    raise NotImplementedError("Operand {} could not be assembled".format(operand))

@assemble_operand.register(Inherent)
def _(operand):
    return ()

@assemble_operand.register(Immediate)
def _(operand):
    return (operand.value, )

@assemble_operand.register(PageDirect)
def _(operand):
    return (operand.address, )


def hi(b):
    return b >> 8

def lo(b):
    return b & 0xFF
