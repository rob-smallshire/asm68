
class Label:

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._name)