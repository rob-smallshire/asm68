import reprlib
from numbers import Integral

from asm68.addrmodecodes import INH, IMM, DIR, IDX, EXT, REL8
from asm68.label import Label


class Inherent:

    codes = {INH}

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return True

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def __hash__(self):
        return hash(self.__class__)


class Immediate:

    codes = {IMM}

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._value)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._value == rhs._value

    def __hash__(self):
        return hash(self._value)


class Registers:

    codes = {IMM}

    def __init__(self, registers):
        if len(registers) < 1:
            raise ValueError("At least one register must be specified.")
        self._registers = registers

    @property
    def registers(self):
        return self._registers

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._registers)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._registers == rhs._registers

    def __hash__(self):
        return hash(self._registers)


class PageDirect:

    codes = {DIR}

    def __init__(self, address):
        if not (0 <= address <= 0xFF):
            raise ValueError("Invalid page direct address 0x{:X}. "
                             "Must be one byte 0x00-0xFF.".format(address))
        self._address = address

    @property
    def address(self):
        return self._address

    def __repr__(self):
        return "{}(0x{:02X})".format(self.__class__.__name__, self._address)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._address == rhs._address

    def __hash__(self):
        return hash(self._address)


class ExtendedDirect:

    codes = {EXT}

    def __init__(self, address):
        if not isinstance(address, (Integral, Label)):
            raise TypeError("Integer address or label expected, got {!r}".format(address))
        if isinstance(address, Integral) and not (0x0000 <= address <= 0xFFFF):
            raise ValueError("Invalid extended direct address 0x{:X}. "
                             "Must be one two byte 0x0000-0xFFFF.".format(address))
        self._address = address
        self._key = (self.__class__, self._address)

    @property
    def address(self):
        return self._address

    def __repr__(self):
        field = "0x{:04X}".format(self._address) if isinstance(self._address, Integral) else str(self._address)
        return "{}({})".format(self.__class__.__name__, field)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._key == rhs._key

    def __hash__(self):
        return hash(self._key)




class ExtendedIndirect:

    codes = {EXT}

    def __init__(self, address):
        if not isinstance(address, (Integral, Label)):
            raise TypeError("Integer address or label expected, got {!r}".format(address))
        if isinstance(address, Integral) and not (0x0000 <= address <= 0xFFFF):
            raise ValueError("Invalid extended indirect address 0x{:X}. "
                             "Must be 0x0000-0xFFFF.".format(address))
        self._address = address
        self._key = (self.__class__, self._address)

    @property
    def address(self):
        return self._address

    def __repr__(self):
        field = "0x{:04X}".format(self._address) if isinstance(self._address, Integral) else str(self._address)
        return "{}({})".format(self.__class__.__name__, field)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._key == rhs._key

    def __hash__(self):
        return hash(self._key)


class Indexed:

    codes = {IDX}

    def __init__(self, base, offset):
        self._base = base
        self._offset = offset

    @property
    def base(self):
        return self._base

    @property
    def offset(self):
        return self._offset

    def __repr__(self):
        return "{}(base={}, offset={})".format(self.__class__.__name__, self._base, self._offset)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return (self._base == rhs._base) and (self._offset == rhs._offset)

    def __hash__(self):
        return hash((self._base, self._offset))


class Relative:

    codes = {REL8}

    def __init__(self, offset):
        if not (0x00 <= offset <= 0xFF):
            raise ValueError("Relative address 0x{:02X} out of range 0x00-0xFF".format(offset))
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._offset)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._offset == rhs._offset

    def __hash__(self):
        return hash(self._offset)


# TODO: This isn't really an addressing mode
class Integers:

    def __init__(self, items):
        if len(items) < 1:
            raise ValueError("At least one integer must be provided")
        if not all(isinstance(item, Integral) for item in items):
            raise TypeError("Not all items in {} are of integral type".format(reprlib.repr(items)))
        self._items = tuple(items)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._items)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._items == rhs._items

    def __hash__(self):
        return hash(self._items)

    def __getitem__(self, index):
        return self._items[index]

