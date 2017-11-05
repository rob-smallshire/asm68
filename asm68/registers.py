from numbers import Integral


class Register:

    _names_and_widths = {}

    def __init__(self, name, width=None):
        if len(name) < 1:
            raise ValueError("Register name cannot be empty")

        if not name.isupper():
            raise ValueError(f"Register name {name!r} is not uppercase letters")

        if (width is not None) and (width < 1):
            raise ValueError(f"Register width {width} is not at least one")

        if name in Register._names_and_widths:
            existing_width = Register._names_and_widths[name]
            if width is None:
                width = existing_width
            elif width != existing_width:
                raise ValueError("Inconsistent register width {} for {} register."
                                 "Previous width was {}".format(width, name, existing_width))

        if width is None:
            raise ValueError("Unspecified register width")

        self._name = name
        self._width = width
        Register._names_and_widths[name] = width

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

    def __add__(self, rhs):
        if not isinstance(rhs, Integral):
            return NotImplemented
        return Crement(self, +rhs)

    def __rsub__(self, lhs):
        if not isinstance(lhs, Integral):
            return NotImplemented
        return Crement(self, -lhs)

class Crement:

    def __init__(self, register, delta):
        if delta not in {-2, -1, +1, +2}:
            direction = 'post-inc' if delta > 0 else 'pre-dec'
            raise ValueError(f"Auto {direction}rement {delta} of {register.name} not in the range 0 to 2")
        self._register = register
        self._delta = delta

    @property
    def register(self):
        return self._register

    @property
    def delta(self):
        return self._delta

    def __repr__(self):
        return "{}({}, {:+})".format(self.__class__.__name__, self.register, self.delta)

    def __eq__(self, rhs):
        if not isinstance(rhs, Crement):
            return NotImplemented
        return (self.delta == rhs.delta) and (self.register == rhs.register)

    def __hash__(self):
        return hash((self.delta, self.register))

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