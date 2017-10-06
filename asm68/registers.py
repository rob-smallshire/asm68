class RegisterName:

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

A = RegisterName('A')
B = RegisterName('B')
X = RegisterName('X')
Y = RegisterName('Y')
U = RegisterName('U')
S = RegisterName('S')
PC = RegisterName('PC')
PCR = RegisterName('PCR')
DP = RegisterName('DP')
CC = RegisterName('CC')
