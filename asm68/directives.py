from asm68.mnemonics import ORG
from asm68.statement import Statement


class Directive(Statement):
    pass

class Org(Directive):
    mnemonic = ORG
