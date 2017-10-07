
class Label:

    def __init__(self, name):
        self._name = name
        self._key = (self.__class__, self._name)

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._name)

    def __eq__(self, rhs):
        if not isinstance(rhs, Label):
            return NotImplemented
        return self._key == rhs._key

    def __hash__(self):
        return hash(self._key)
