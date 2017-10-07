class Register:

    _instances = {}

    def __new__(cls, name):
        if name in cls._instances:
            return cls._instances[name]
        obj = object.__new__(cls)
        obj._name = name
        cls._instances[name] = obj
        return obj

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._name)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._name == rhs._name

    def __hash__(self):
        return hash(self._name)

A = Register('A')
B = Register('B')
X = Register('X')
Y = Register('Y')
U = Register('U')
S = Register('S')
PC = Register('PC')
PCR = Register('PCR')
DP = Register('DP')
CC = Register('CC')
