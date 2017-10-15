from asm68.asmdsl import AsmDsl, statements
from asm68.assembler import assemble
from asm68.mnemonics import *


def test_leventhal_4_1__8_bit_data_transfer():
    asm = AsmDsl()
    asm     (   LDA,    {0x40},     "GET DATA"                  )
    asm     (   STA,    {0x41},     "TRANSFER to NEW LOCATION"  )
    asm     (   SWI                                             )

    code = assemble(statements(asm))
    assert code == bytes.fromhex(
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
    assert code == bytes.fromhex(
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
    assert code == bytes.fromhex(
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
    assert code == bytes.fromhex(
        '96 40'
        '84 0F'
        '97 41'
        '3F')

def test_leventhal_4_5__clear_a_memory_location():
    asm = AsmDsl()
    asm     (   CLR,    {0x40},     "CLEAR MEMORY LOCATION 0040")
    asm     (   SWI                                             )

    code = assemble(statements(asm))
    assert code == bytes.fromhex(
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
    assert code == bytes.fromhex(
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
    assert code == bytes.fromhex(
        '96 40'
        '91 41'
        '24 02'
        '96 41'
        '97 42'
        '3F')
