from asm68.asmdsl import AsmDsl, statements
from asm68.assembler import assemble
from asm68.mnemonics import *
from asm68.registers import B, X


def test_leventhal_4_1__8_bit_data_transfer():
    asm = AsmDsl()
    asm     (   LDA,    {0x40},     "GET DATA"                  )
    asm     (   STA,    {0x41},     "TRANSFER to NEW LOCATION"  )
    asm     (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '96 40'
        '97 41'
        '3F')

def test_leventhal_4_2__8_bit_addition():
    asm = AsmDsl()
    asm     (   LDA,    {0x40},     "GET FIRST OPERAND"         )
    asm     (   ADDA,   {0x41},     "ADD SECOND OPERAND"        )
    asm     (   STA,    {0x42},     "STORE RESULT"              )
    asm     (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '96 40'
        '9B 41'
        '97 42'
        '3F')

def test_leventhal_4_3__shift_left_1_bit():
    asm = AsmDsl()
    asm     (   LDB,    {0x40},     "GET DATA"                  )
    asm     (   ASLB,               "SHIFT LEFT"                )
    asm     (   STB,    {0x41},     "STORE RESULT"              )
    asm     (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        'D6 40'
        '58'
        'D7 41'
        '3F')

def test_leventhal_4_4__8_bit_addition():
    asm = AsmDsl()
    asm     (   LDA,    {0x40},     "GET DATA"                  )
    asm     (   ANDA,   0b00001111, "MASK OUT FOR MSB'S"        )
    asm     (   STA,    {0x41},     "STORE RESULT"              )
    asm     (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '96 40'
        '84 0F'
        '97 41'
        '3F')

def test_leventhal_4_5__clear_a_memory_location():
    asm = AsmDsl()
    asm     (   CLR,    {0x40},     "CLEAR MEMORY LOCATION 0040")
    asm     (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '0F 40'
        '3F')

def test_leventhal_4_6__byte_disassembly():
    asm = AsmDsl()
    asm     (   LDA,    {0x40},     "GET DATA"                  )
    asm     (   ANDA,   0b00001111, "MASK OFF MSB'S"            )
    asm     (   STA,    {0x42},     "STORE LSB'S"               )
    asm     (   LDA,    {0x40},     "RELOAD DATA"               )
    asm     (   LSRA,               "SHIFT MSB'S TO LEAST"      )
    asm     (   LSRA,               "SIGNIFICANT POSITIONS"     )
    asm     (   LSRA,               "AND CLEAR OTHER"           )
    asm     (   LSRA,               "POSITIONS"                 )
    asm     (   STA,    {0x41},     "STORE MSB'S"               )
    asm     (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '96 40'
        '84 0F'
        '97 42'
        '96 40'
        '44'
        '44'
        '44'
        '44'
        '97 41'
        '3F')

def test_leventhal_4_7__find_larger_of_two_numbers():
    asm = AsmDsl()
    asm        (   LDA,    {0x40},     "GET FIRST OPERAND"         )
    asm        (   CMPA,   {0x41},     "IS SECOND OPERAND LARGER?" )
    asm        (   BHS,    asm.stres                               )
    asm        (   LDA,    {0x41},     "YES,GET SECOND OPERAND"    )
    asm .stres (   STA,    {0x42},     "STORE LARGER OPERAND"      )
    asm        (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '96 40'
        '91 41'
        '24 02'
        '96 41'
        '97 42'
        '3F')

def test_levethal_4_8__sixteen_bit_addition():
    asm = AsmDsl()
    asm         (   LDD,    {0x40},     "GET FIRST 16-BIT NUMBER"   )
    asm         (   ADDD,   {0x42},     "ADD SECOND 16-BIT NUMBER"  )
    asm         (   STD,    {0x44},     "STORE 16-BIT RESULT"       )
    asm         (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        'DC 40'
        'D3 42'
        'DD 44'
        '3F')

def test_levethal_4_9__table_of_squares():
    asm = AsmDsl()
    asm         (   LDB,    {0x41},     "GET DATA"                  )
    asm         (   LDX,    0x50,       "GET BASE ADDRESS"          )
    asm         (   LDA,    {B:X},      "GET SQUARE OF DATA"        )
    asm         (   STA,    {0x42},     "STORE SQUARE"              )
    asm         (   SWI                                             )
    asm         (   ORG,    0x50,       "TABLE OF SQUARES"          )
    asm .SQTAB  (   FCB,    (0, 1, 4, 9, 16, 25, 36, 49)            )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        'D6 41'
        '8E 0050'
        'A6 85'
        '97 42'
        '3F')

    assert code[0x50] == bytes.fromhex(
        '00 01 04 09 10 19 24 31'
    )

def test_levethal_4_9_modified__table_of_squares():
    asm = AsmDsl()
    asm         (   LDB,    {0x41},     "GET DATA"                  )
    asm         (   LDX,    asm.SQTAB,  "GET BASE ADDRESS"          )
    asm         (   LDA,    {B:X},      "GET SQUARE OF DATA"        )
    asm         (   STA,    {0x42},     "STORE SQUARE"              )
    asm         (   SWI                                             )
    asm         (   ORG,    0x50,       "TABLE OF SQUARES"          )
    asm .SQTAB  (   FCB,    (0, 1, 4, 9, 16, 25, 36, 49)            )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        'D6 41'
        '8E 0050'
        'A6 85'
        '97 42'
        '3F')

    assert code[0x50] == bytes.fromhex(
        '00 01 04 09 10 19 24 31'
    )