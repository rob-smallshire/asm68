import reprlib
import weakref
from functools import singledispatch

from asm68.addrmodes import Immediate, Inherent, PageDirect, ExtendedDirect, ExtendedIndirect, Registers, Indexed, \
     Integers
from asm68.mnemonicmap import MNEMONIC_TO_STATEMENT
from asm68.label import Label
from numbers import Integral
from collections.abc import Set

from asm68.registers import Register, AutoIncrementedRegister


class AsmDsl:

    def __init__(self):
        self._statements = []
        self._label_statement_index = {}

    def __call__(self, mnemonic, *args, label=None):
        operand = None
        comment = ""
        if len(args) == 0:
            pass
        elif len(args) == 1:
            if isinstance(args[0], str):
                comment = args[0]
            else:
                operand = args[0]
        elif len(args) == 2:
            operand, comment = args
        else:
            raise TypeError("Unhandled number are assembler arguments")

        if label is not None:
            self._label_statement_index[label] = len(self._statements)

        operand_node = parse_operand(operand)

        if mnemonic not in MNEMONIC_TO_STATEMENT:
            raise ValueError("No such opcode matching mnemonic {}".format(mnemonic))
        statement_node = MNEMONIC_TO_STATEMENT[mnemonic](operand_node, comment, label)
        self._statements.append(statement_node)

    def __getattr__(self, name):
        return Labeller(self, name=name)


class Labeller(Label):

    def __init__(self, asm, name):
        super().__init__(name)
        self._asm = weakref.ref(asm)

    def __call__(self, *args, **kwargs):
        asm = self._asm()
        if asm is None:
            raise RuntimeError("AsmDsl instance no longer available.")
        return asm(*args, label=self.name, **kwargs)

def statements(asm):
    return tuple(asm._statements)

def statement_index(asm, label):
    return asm._label_statement_index[label]


@singledispatch
def parse_operand(operand):
    raise TypeError("Unrecognised operand type {!r}".format(operand))

@parse_operand.register(type(None))
def _(operand):
    assert operand is None
    return Inherent()

@parse_operand.register(Integral)
def _(operand):
    return Immediate(operand)

@parse_operand.register(bytes)
def _(operand):
    try:
        byte = single(operand)
    except ValueError as ve:
        raise ValueError("Immediate8 string operand must contain an single ASCII character. Got {} in {!r}".format(len(operand), operand)) from ve

    return Immediate(byte)

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
    if all(isinstance(item, Register) for item in operand):
        return Registers(operand)
    elif all(isinstance(item, Integral) for item in operand):
        return Integers(operand)
    else:
        raise TypeError("{} could not be parsed".format(operand))

@parse_operand.register(list)
def _(operand):
    item = single(operand)
    return parse_indirect_operand(item)

@parse_operand.register(dict)
def _(operand):
    offset, base = single(operand.items())
    if not isinstance(offset, (Register, Integral)):
        raise TypeError("Expected integer offset. Got {}".format(offset))
    if not isinstance(base, (Register, AutoIncrementedRegister)):
        raise TypeError("{} is not a base".format(base))
    return Indexed(base=base, offset=offset)

@parse_operand.register(Label)
def _(operand):
    # TODO: Label is not an addressing mode, so this should be replaced with Relative or ExtendedDirect depending on what the instruction supports
    return operand


@singledispatch
def parse_indirect_operand(operand):
    raise TypeError("Unrecognised indirect operand type {!r}".format(operand))

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
#     return Immediate8(operand)
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


