from asm68.opcodes import OPCODES
from asm68.util import typename


class Mnemonic:

    def __init__(self, opcode_key):
        if len(opcode_key) == 0:
            raise ValueError("Opcode key cannot be empty")
        if not opcode_key[0].isalpha():
            raise ValueError("Opcode key {opcode_key!r} does not start with a letter")
        self._mnemonic = opcode_key.upper()
        self._opcode_key = opcode_key

    @property
    def key(self):
        return self._opcode_key

    def __str__(self):
        return self._mnemonic

    def __repr__(self):
        return "{}({})".format(typename(self), self._mnemonic)

    def __hash__(self):
        return hash(self._mnemonic)

    def __eq__(self, other):
        if not isinstance(other, Mnemonic):
            return NotImplemented
        return self._mnemonic == other._mnemonic


for opcode_key in OPCODES:
    mnemonic = Mnemonic(opcode_key)
    globals()[str(mnemonic)] = mnemonic


ORG = Mnemonic('ORG')
FCB = Mnemonic('FCB')
FDB = Mnemonic('FDB')
CALL = Mnemonic('CALL')
# TODO: Setdp

