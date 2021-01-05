import weakref
from collections.abc import Set, Callable
from functools import singledispatch
from numbers import Integral

from asm68.addrmodes import (Immediate, Inherent, PageDirect, ExtendedDirect,
                             ExtendedIndirect, Registers, Indexed, Integers)
from asm68.label import Label
from asm68.mnemonicmap import MNEMONIC_TO_STATEMENT
from asm68.registers import Register, AutoIncrementedRegister
from asm68.util import single
from asm68.integers import U8, U16, U32, I8, I16, I32

PROGRAM_COUNTER_LABEL_NAME = "pc"


class AsmDsl:

    def __init__(self):
        self._statements = []
        self._label_statement_index = {}

    def __call__(self, mnemonic, *args, label=None):
        statement_node = self.statement(mnemonic, *args, label=label)
        self._statements.append(statement_node)

    def statement(self, mnemonic, *args, label=None):
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
        return statement_node

    @property
    def pc(self):
        return ProgramCounterLabel(self)

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

    def __getattr__(self, name):
        asm = self._asm()
        if asm is None:
            raise RuntimeError("AsmDsl instance no longer available.")
        return Labeller(asm, name=name)


class ProgramCounterLabel(Label):
    """A special label which points to the program counter."""

    def __init__(self, asm):
        super().__init__(PROGRAM_COUNTER_LABEL_NAME)
        self._asm = weakref.ref(asm)


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

@parse_operand.register(Callable)
def _(operand):
    return operand

@parse_operand.register(Integral)
def _(operand):
    """Parse an immediate operand.

    Immediate operands are simple values such as 0, 0x10, or 0b10101010, or an expression evaluating
    to such a value, such as ord("A").
    """
    return Immediate(operand)

@parse_operand.register(bytes)
def _(operand):
    return Immediate(int.from_bytes(operand, byteorder="big", signed=False), len(operand))


@parse_operand.register(U8)
def _(operand):
    return Immediate(operand.value, 1)


@parse_operand.register(U16)
def _(operand):
    return Immediate(operand.value, 2)


@parse_operand.register(U32)
def _(operand):
    return Immediate(operand.value, 4)


@parse_operand.register(I8)
def _(operand):
    return Immediate(int.from_bytes(
        operand.value.to_bytes(1, byteorder="big", signed=True),
        byteorder="big",
        signed=False
    ), 1)


@parse_operand.register(I16)
def _(operand):
    unsigned = operand.value.to_bytes(2, byteorder="big", signed=True)
    return Immediate(int.from_bytes(
        unsigned,
        byteorder="big",
        signed=False
    ), 2)


@parse_operand.register(I32)
def _(operand):
    return Immediate(int.from_bytes(
        operand.value.to_bytes(4, byteorder="big", signed=True),
        byteorder="big",
        signed=False
    ), 4)


@parse_operand.register(Set)
def _(operand):
    item = single(operand)
    return parse_direct_operand(item)

@parse_operand.register(tuple)
def _(operand):
    if all(isinstance(item, Register) for item in operand):
        return Registers(operand)
    elif all(isinstance(item, (Integral, Label)) for item in operand):
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

@singledispatch
def parse_direct_operand(item):
    raise TypeError("Unrecognised direct operand type {!r}".format(item))

@parse_direct_operand.register(Label)
def _(item):
    return ExtendedDirect(item)

@parse_direct_operand.register(Integral)
def _(item):
    if item < 0:
        raise ValueError("Direct address {} is negative.".format(item))
    if item <= 0xFF:
        return PageDirect(item)
    if item <= 0xFFFF:
        return ExtendedDirect(item)
    raise ValueError("Direct address 0x{:X} out of range 0x0000-0xFFFF".format(item))

@parse_direct_operand.register(U8)
def _(item):
    return PageDirect(item.value)

@parse_direct_operand.register(U16)
def _(item):
    return ExtendedDirect(item.value)

