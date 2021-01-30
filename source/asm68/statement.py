from abc import ABC


class Statement(ABC):

    _mnemonic_map = {}

    mnemonic = None

    def __init_subclass__(cls, **kwargs):
        print(cls, kwargs, hasattr(cls, "mnemonic") and cls.mnemonic)
        if cls.mnemonic is not None:
            cls._mnemonic_map[cls.mnemonic] = cls

    @classmethod
    def from_mnemonic(cls, mnemonic, operand, comment=None, label=None):
        try:
            subclass = cls._mnemonic_map[mnemonic]
        except KeyError:
            raise ValueError(f"No statement matching mnemonic {mnemonic}")
        return subclass(operand, comment, label)

    def __init__(self, operand, comment=None, label=None):
        if self.mnemonic is None:
            raise NotImplementedError("Statement class {} does not override mnemonic".format(self.__class__))

        self._operand = operand
        self._comment = comment or ''
        self._label = label

    def __repr__(self):
        return "{}(operand={!r}, label={!r})".format(self.__class__.__name__, self._operand, self._label)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._is_equal(rhs)

    def __hash__(self):
        return hash((self.mnemonic, self.operand, self.comment, self.label))

    def _is_equal(self, rhs):
        return (self.mnemonic == rhs.mnemonic) and (self._operand == rhs._operand) and (self._comment == rhs._comment) and (self._label == rhs._label)

    @property
    def operand(self):
        return self._operand

    @property
    def comment(self):
        return self._comment

    @property
    def label(self):
        return self._label