from asm6x.mnemonics import (ORG, FCB)
from asm6x.statement import Statement


class Directive(Statement):
    pass

class Org(Directive):
    mnemonic = ORG

class Fcb(Directive):
    mnemonic = FCB
