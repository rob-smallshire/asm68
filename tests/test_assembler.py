from hypothesis import given
from hypothesis.strategies import lists, one_of, integers
from pytest import raises

from asm6x.asmdsl import AsmDsl, statements
from asm6x.assembler import assemble, assemble_statement, assemble_operand
from asm6x.mnemonics import *
from asm6x.registers import B, X, A


def test_assemble_unsupported_statement_type_raises_type_error():
    with raises(TypeError):
        assemble_statement(object(), None)

def test_assemble_unsupported_operand_type_raises_type_error():
    with raises(TypeError):
        assemble_operand(object(), None, None, None)

def test_assemble_org_without_immediate_operand_raises_type_error():
    asm = AsmDsl()
    asm         (   ORG,    {0x03},       "ILLEGAL ADDRESS MODE"    )
    s = statements(asm)
    with raises(TypeError):
        assemble(s)

def test_origin_address_lies_within_existing_code_fragment():
    asm = AsmDsl()
    asm         (   LDB,    {0x41},     "GET DATA"                  )
    asm         (   LDX,    asm.SQTAB,  "GET BASE ADDRESS"          )
    asm         (   LDA,    {B:X},      "GET SQUARE OF DATA"        )
    asm         (   STA,    {0x42},     "STORE SQUARE"              )
    asm         (   SWI                                             )
    asm         (   ORG,    0x03,       "TABLE OF SQUARES"          )

    s = statements(asm)

    with raises(ValueError):
        assemble(s)

def test_fcb_operand_is_not_integers_raises_type_error():
    asm = AsmDsl()
    asm         (   FCB,    0            )
    s = statements(asm)
    with raises(TypeError):
        assemble(s)

@given(items=lists(min_size=1, elements=one_of(integers(max_value=-1), integers(min_value=256))))
def test_fcb_operand_integers_out_of_range_raises_value_error(items):
    asm = AsmDsl()
    asm         (   FCB,    tuple(items)            )
    s = statements(asm)
    with raises(ValueError):
        assemble(s)

def test_label_reuse_raises_runtime_error():
    asm = AsmDsl()
    asm        (   LDA,    {0x40},     "GET FIRST OPERAND"         )
    asm        (   CMPA,   {0x41},     "IS SECOND OPERAND LARGER?" )
    asm        (   BHS,    asm.stres                               )
    asm        (   LDA,    {0x41},     "YES,GET SECOND OPERAND"    )
    asm .stres (   STA,    {0x42},     "STORE LARGER OPERAND"      )
    asm .stres (   SWI                                             )
    s = statements(asm)
    with raises(RuntimeError):
        assemble(s)

def test_incorrect_index_register_raises_value_error():
    asm = AsmDsl()
    asm         (   LDA,    {B:A},      "GET SQUARE OF DATA"        )
    s = statements(asm)
    with raises(ValueError):
        assemble(s)


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