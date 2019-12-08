from asm68.asmdsl import AsmDsl
from asm68.mnemonics import (FDB, ORG, NOP, JMP)

asm = AsmDsl()

asm         (   ORG,   0xC000,  "Bottom of the top 16 K ROM"    )

asm .BEGIN  (   NOP,             "Do nothing"                   )

for i in range(0xC001, 0xFFFF - 16 - 3 + 1):
    asm     (   NOP,             "Do nothing"                   )
    
asm .JUMP   (   JMP,   asm.BEGIN, "Jump back to the bottom"     )

# Vector table at top of memory
asm         (   FDB,   (0xC000,     # Reserved
                        0xC000,     # SWI3
                        0xC000,     # SWI2
                        0xC000,     # /FIRQ
                        0xC000,     # /IRQ
                        0xC000,     # SWI
                        0xC000,     # /NMI
                        0xC000,     # /RESET
                               )                                )
