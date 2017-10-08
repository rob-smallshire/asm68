from numbers import Integral

from asm68.addrmodecodes import INH, IMM, DIR, IDX, EXT, REL
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
        self._key = (self.__class__, self._value)

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._value)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._key == rhs._key

    def __hash__(self):
        return hash(self._key)


class Registers:

    codes = {IMM}

    def __init__(self, registers):
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
        self._key = (self.__class__, self._address)

    @property
    def address(self):
        return self._address

    def __repr__(self):
        return "{}(0x{:02X})".format(self.__class__.__name__, self._address)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._key == rhs._key

    def __hash__(self):
        return hash(self._key)


class ExtendedDirect:

    codes = {EXT}

    def __init__(self, address):
        if not isinstance(address, (Integral, Label)):
            raise TypeError("Integer address or label expected, got {!r}".format(address))
        if isinstance(address, Integral) and not (0x0100 <= address <= 0xFFFF):
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
        return "{}(0x{:04X})".format(self.__class__.__name__, field)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._key == rhs._key

    def __hash__(self):
        return hash(self._key)


class Indexed:

    codes = {IDX}

    def __init__(self, register, offset):
        self._register = register
        self._offset = offset

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, self._register, self._offset)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return (self._register == rhs._register) and (self._offset == rhs._offset)

    def __hash__(self):
        return hash((self._register, self._offset))


class Relative:

    codes = {REL}

    def __init__(self, offset):
        self._offset = offset

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._offset)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._offset == rhs._offset

    def __hash__(self):
        return hash(self._offset)


