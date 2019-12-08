from asm68.mnemonics import (ORG, FCB, FDB)
from asm68.statement import Statement


class Directive(Statement):
    pass

class Org(Directive):
    mnemonic = ORG

class Fcb(Directive):
    mnemonic = FCB
    
class Fdb(Directive):
    mnemonic = FDB

