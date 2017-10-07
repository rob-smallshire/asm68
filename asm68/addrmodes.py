from numbers import Integral

from asm68.label import Label


class Inherent:

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return True

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def __hash__(self):
        return hash(self.__class__)

class Immediate:

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



class PageDirect:

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

# TODO: Indexed addressing

class Indexed:
    pass

INH = "Inherent"
IMM = "Immediate"
DIR = "Direct"
IDX = "Indexed"
EXT = "Extended"

ADDRESSING_MODE_CODES = {
    Inherent: INH,
    Immediate: IMM,
    PageDirect: DIR,
    Indexed: IDX,
    ExtendedDirect: EXT,
    ExtendedIndirect: EXT,
}