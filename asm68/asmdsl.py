import reprlib
import types
from functools import singledispatch

from asm68.addrmodes import Immediate, Inherent, PageDirect, ExtendedDirect, ExtendedIndirect, Registers
from asm68.ast import MNEMONIC_TO_AST
from asm68.label import Label
from numbers import Integral
from collections.abc import Set

from asm68.registers import Register

class AsmDsl:

    def __init__(self):
        self._statements = []

    def __call__(self, mnemonic, operand=None):

        operand_node = parse_operand(operand)

        if mnemonic not in MNEMONIC_TO_AST:
            raise ValueError("No such opcode matching mnemonic {}".format(mnemonic))
        statement_node = MNEMONIC_TO_AST[mnemonic](operand_node)
        self._statements.append(statement_node)

    @property
    def statements(self):
        return tuple(self._statements)


# class AsmDsl:
#
#     def __init__(self):
#         self._labels = {}
#
#     def __call__(self, opcode, *args):
#         if len(args) == 1:
#             if isinstance(args[0], str):
#                 operand = None
#                 comment = args[0]
#             else:
#                 operand = args[0]
#                 comment = ""
#         elif len(args) == 2:
#             operand, comment = args
#         else:
#             raise TypeError("Incorrect argument types.")
#
#         if not isinstance(comment, str):
#             raise TypeError("Comment must be a string")
#
#         address = self._asm(opcode, operand, comment)
#         return address
#
#
#     def _asm(self, opcode, operand, comment):
#         # Create a statement
#         if opcode not in OPCODES:
#             raise ValueError("No such opcde: {}".format(opcode))
#
#         parse_operand(operand)
#
#         return address
#
#     def __getattr__(self, name):
#         return Labeller(self, label=name)
#
# class Labeller:
#
#     def __init__(self, asm, label):
#         self._asm = asm
#         self._label = label
#
#     def __call__(self, *args, **kwargs):
#         address = self._asm(*args, **kwargs)
#         self._asm._labels[self._label] = address
#         return address


@singledispatch
def parse_operand(operand):
    raise NotImplementedError("Unrecognised operand type".format(operand))

@parse_operand.register(type(None))
def _(operand):
    assert operand is None
    return Inherent()

@parse_operand.register(Integral)
def _(operand):
    return Immediate(operand)

@parse_operand.register(Integral)
def _(operand):
    return Immediate(operand)

@parse_operand.register(Set)
def _(operand):
    item = single(operand)
    if isinstance(item, Label):
        return ExtendedDirect(item)
    elif isinstance(item, Integral):
        if item < 0:
            raise ValueError("Direct address {} is negative.".format(operand))
        if item <= 0xFF:
            return PageDirect(item)
        if item <= 0xFFFF:
            return ExtendedDirect(item)
        raise ValueError("Direct address 0x{:X} out of range 0x0000-0xFFFF".format(item))
    else:
        raise TypeError("Expected integer address or label. Got {}".format(item))

@parse_operand.register(tuple)
def _(operand):
    for item in operand:
        if not isinstance(item, Register):
            raise TypeError("{} is not a register".format(item))
    return Registers(operand)

@parse_operand.register(list)
def _(operand):
    item = single(operand)
    return parse_indirect_operand(item)



@singledispatch
def parse_indirect_operand(operand):
    raise NotImplementedError("Unrecognised indirect operand type".format(operand))

@parse_indirect_operand.register(Set)
def _(operand):
    item = single(operand)
    if isinstance(item, Label):
        return ExtendedIndirect(item)
    elif isinstance(item, Integral):
        if item < 0:
            raise ValueError("Direct address {} is negative.".format(operand))
        if item <= 0xFFFF:
            return ExtendedIndirect(item)
        raise ValueError("Indirect address 0x{:X} out of range 0x0000-0xFFFF".format(item))
    else:
        raise TypeError("Expected integer address or label. Got {}".format(item))



def single(iterable):
    i = iter(iterable)
    try:
        value = next(i)
    except StopIteration:
        raise ValueError("Expected one item. Too few items in {}".format(reprlib.repr(iterable)))
    try:
        next(i)
        raise ValueError("Expected one item. Too many items in {}".format(reprlib.repr(iterable)))
    except StopIteration:
        return value

#
# @parse_operand.register(type(None))
# def inherent(operand):
#     return Inherent()
#
#
# @parse_operand.register(Integral)
# def immediate(operand):
#     # TODO: Validation
#     return Immediate(operand)
#
#
# @parse_operand.register(Set)
# def direct(operand):
#     if len(operand) != 1:
#         raise TypeError("Could not parse {}. Direct addressing mode has form {{address}} with a "
#                         "single address.".format(operand))
#     item = next(operand)
#     if isinstance(item, Integral):
#         if item < 0:
#             raise ValueError("Direct address {} is negative.".format(item))
#         if item <= 0xFF:
#             return PageDirect(item)
#         if item <= 0xFFFF:
#             return ExtendedDirect(item)
#         raise ValueError("Direct address 0x{:04X} out of range 0x0000-0xFFFF".format(item))
#     elif isinstance(item, Label):
#         return ExtendedDirect(label)
#     else:
#         raise TypeError("Expected integer address or label. Got {}".format(operand))
#
#
# @parse_operand.register(tuple)
# def indexed(operand):
#     if len(operand) == 1:
#         r = operand[0]
#         if not isinstance(r, Register):
#             raise TypeError("{} is not a register name. The first element of zero-offset indexed address "
#                             "must be a register name".format(r))
#         return ZeroOffsetIndexed(r)
#
#     elif len(operand) == 2:
#         r, offset = operand
#         if not isinstance(r, Register):
#             raise TypeError("{} is not a register name. The first element of zero-offset indexed address "
#                             "must be a register name".format(r))
#         if r == PCR:
#             if isinstance(offset, Integral):
#                 if not (0 <= offset <= 0xFFFF):
#                     raise ValueError("0x{:04X} offset out of range 0x0000-0xFFFF.")
#                 return ProgramCounterRelativeIndexed(offset)
#             elif isinstance(offset, Label):
#                 return ProgramCounterRelativeIndexed(offset)
#             else:
#                 raise TypeError("{} cannot be used as the target for program counter relative (PCR) addressing".format(offset))
#         else:
#             if isinstance(offset, Integral):
#                 if not (-32768 <= offset <= 32767):
#                     raise ValueError("{:X} offset out of range -0x8000 to 0x7FFF.")
#             return ConstantOffsetIndexed(r, offset)
#
#     elif len(operand == 3):
#         # Pre-/Post- Increment/Decrement
#         (Integral, Register, Integral)
#
#     else:
#         raise TypeError("Indexed addressing mode can have only 1, 2 or 3 arguments.")
#


