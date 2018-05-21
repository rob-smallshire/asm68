from asm68.asmdsl import AsmDsl
from asm68.mnemonics import (LDB, LDX, LDA, INCB, CMPA, BNE, STB, SWI)
from asm68.registers import X


asm = AsmDsl()

asm         (   LDB,    0xFF,        "STRING LENGTH = -1"            )
asm         (   LDX,    0x41,        "POINT TO START OF STRING"      )
asm         (   LDA,    0x0D,        "GET ASCII CARRIAGE RETURN "
                                          "(STRING TERMINATOR)"      )
asm  .CHKCR (   INCB,                "ADD 1 TO STRING LENGTH"        )
asm         (   CMPA,   {0:X+1},     "IS NEXT CHARACTER "
                                              "A CARRIAGE RETURN?"   )
asm         (   BNE,    asm.CHKCR,   "NO, KEEP CHECKING"             )
asm  .DONE  (   STB,    {0x40},      "YES, SAVE STRING LENGTH"       )
asm         (   SWI                                                  )
