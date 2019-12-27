from asm68.addrmodecodes import REL8, REL16, IMM, EXT
from asm68.util import is_valid_variable_name


class Label:

    CODES = frozenset({
        REL8,
        REL16,
        IMM,
    })

    def __init__(self, name):
        if (not is_valid_variable_name(name)) or name.startswith('_'):
            raise ValueError("{!r} is not a valid label name".format(name))
        self._name = name

    @property
    def codes(self):
        return self.CODES

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._name)

    def __eq__(self, rhs):
        if not isinstance(rhs, Label):
            return NotImplemented
        return self._name == rhs._name

    def __hash__(self):
        return hash(self._name)
