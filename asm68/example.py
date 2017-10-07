from asm68.asmdsl import AsmDsl
from asm68.mnemonics import *
from asm68.registers import *

asm = AsmDsl()




block = 45

asm       ( ASRA,                 "Shift accumlator A right one bit")
asm       ( LDA,  'a'
asm       ( ADDA, 0x30,           "Add 0x30 to accumulator A")
asm       ( ADDD, 0x1057,         "Add 0x1057 to accumulator D")
asm       ( LDS,  0x3F2A,         "Load 0x3F2A to stack pointer S")
asm       ( LDX,  {block},        "Get starting address of block")
asm .loop ( STA,  [(X, 4)],       "Store reading in memory")
asm       ( ADDA, [(X++1 )],      "Add ")
asm       ( ADDA, {0x30},         "Add value at 0x30 offset from DP")
asm       ( ADDA, {0x1C48},       "Add contents of 0x1C48 to accumulator A")
asm       ( ADDA, [{0xD58A}],     "Add the contents of the memory address referred to by the pointer at D58A")
asm       ( ADDA, (X, ),          "Add the contents of the address in X to accumulator A")
asm       ( ADDA, (Y, -1),        "Add the contents of the address one less than that in Y to accumulator A")
asm       ( ADDA, (U, 0x20),      "Add the contents of address 0x20 after stack pointer U to accumulator A")
asm       ( ADDA, (PC, +10),      "Adds the contents of address 0x13 beyond PC to A. Why 13? Because 3-byte instruction.")
asm       ( ADDA, (PCR, asm.loop),"Adds a value at a  PC relative address.")
asm       ( ADDA, [(X, 5)],       "Adds to accumulator A the contents of the address stored five bytes beyond the address in X" )



asm.loop = asm.ldx()
