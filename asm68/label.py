from asm68.addrmodecodes import EXT, REL


class Label:

    codes = {REL, EXT}

    def __init__(self, name):
        self._name = name

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
