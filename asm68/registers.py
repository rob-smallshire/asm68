class Register:

    _instances = {}

    def __new__(cls, name, width=None):
        if len(name) < 1:
            raise ValueError("Register name cannot be empty")

        if not name.isupper():
            raise ValueError(f"Register name {name!r} is not uppercase letters")

        if (width is not None) and (width < 1):
            raise ValueError(f"Register width {width} is not at least one")

        if name in cls._instances:
            instance = cls._instances[name]
            if (width is not None) and (width != instance.width):
                raise ValueError("Inconsistent register width {} for {} register."
                                 "Previous width was {}".format(width, name, instance.width))
            return instance
        if width is None:
            raise ValueError("Unspecified register width")
        obj = object.__new__(cls)
        obj._name = name
        obj._width = width
        cls._instances[name] = obj
        return obj

    @property
    def name(self):
        return self._name

    @property
    def width(self):
        return self._width

    def __str__(self):
        return self._name

    def __repr__(self):
        return "{}({!r}, {})".format(
            self.__class__.__name__, self._name, self._width)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return (self._name == rhs._name) and (self._width == self._width)

    def __lt__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self.name < rhs.name

    def __hash__(self):
        return hash((self._name, self._width))

A = Register('A', 1)
B = Register('B', 1)
D = Register('D', 2)
E = Register('E', 1)
F = Register('F', 1)
W = Register('W', 2)
Q = Register('Q', 4)
X = Register('X', 2)
Y = Register('Y', 2)
U = Register('U', 2)
S = Register('S', 2)
PC = Register('PC', 2)
PCR = Register('PCR', 2)
DP = Register('DP', 1)
CC = Register('CC', 1)
MD = Register('MD', 1)
# TODO: V Register?

INDEX_REGISTERS = {X, Y, U, S}
ACCUMULATORS_1 = {A, B, E, F}
ACCUMULATORS_2 = {D, W}
ACCUMULATORS_4 = {Q}
ACCUMULATORS = ACCUMULATORS_1 | ACCUMULATORS_2 | ACCUMULATORS_4
STATUS_REGISTERS = {DP, CC, MD, PC}
REGISTERS = INDEX_REGISTERS | ACCUMULATORS | STATUS_REGISTERS