import logging
from logging import Handler, NOTSET
from logging.handlers import QueueHandler

import pytest
from hypothesis import given, assume, example
from hypothesis.strategies import lists, one_of, integers, sampled_from
from pytest import raises, skip

from asm68.asmdsl import AsmDsl, statements
from asm68.assembler import assemble, assemble_statement, assemble_operand, TooManyPassesError, \
    Assembler
from asm68.mnemonics import *
from asm68.registers import B, X, A, Y, INDEX_REGISTERS, U, S, E, D, F, W
from asm68.twiddle import twos_complement
from asm68.integers import U8, U16
from asm68.loghandler import ListLogHandler


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
    with raises(ValueError, match=r'FCB value -?\d+ at index \d+ not in range\(0, 256\)'):
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

def test_label_reuse_raises_runtime_error_multiple_segments_created_in_reverse_address_order():
    asm = AsmDsl()
    asm        (   LDA,    {0x40},     "GET FIRST OPERAND"         )
    asm        (   CMPA,   {0x41},     "IS SECOND OPERAND LARGER?" )
    asm        (   BHS,    asm.stres                               )
    asm        (   LDA,    {0x41},     "YES,GET SECOND OPERAND"    )
    asm        (   ORG,    0x50                                    )
    asm .stres (   STA,    {0x42},     "STORE LARGER OPERAND"      )
    asm        (   ORG,    0x30                                    )
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


def test_using_indexed_addressing_offset_register_with_index_register_raises_value_error():
    asm = AsmDsl()
    asm         (   LDA,    {Y:X},      "GET SQUARE OF DATA"        )
    s = statements(asm)
    with raises(ValueError):
        assemble(s)


def test_using_auto_post_increment_with_register_non_index_register_raises_value_error():
    asm = AsmDsl()
    asm         (   LDA,    {0:A+1},      "GET SQUARE OF DATA"        )
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
    asm         (   LDX,    asm.SQTAB,  "GET BASE ADDRESS"          )  # Immediate addressing
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


def test_levethal_4_10_ones_complement():
    asm = AsmDsl()
    asm         (   LDD,    {0x40},     "GET 16-BIT NUMBER"             )
    asm         (   COMA,               "ONES COMPLEMENT MSB'S"         )
    asm         (   COMB,               "ONES COMPLEMENT LSB'S"         )
    asm         (   STD,    {0x42},     "STORE 16-BIT ONES COMPLEMENT"  )
    asm         (   SWI                                                 )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        'DC 40'
        '43'
        '53'
        'DD 42'
        '3F')


def test_levethal_5_1a_sum_of_data():
    asm = AsmDsl()
    asm         (   CLRA,               "SUM = ZERO"                )
    asm         (   LDB,    {0x41},     "COUNT = LENGTH OF ARRAY"   )
    asm         (   LDX,    0x42,       "POINT TO START OF ARRAY"   )
    asm  .SUMD  (   ADDA,   {0:X+1},    "ADD NUMBER TO SUM"         )
    asm         (   DECB                                            )
    asm         (   BNE,    asm.SUMD                                )
    asm         (   STA,    {0x40}                                  )
    asm         (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '4F'
        'D6 41'
        '8E 0042'
        'AB 80'
        '5A'
        '26 FB'
        '97 40'
        '3F')


def test_levethal_5_1b_sum_of_data():
    asm = AsmDsl()
    asm         (   CLRA,               "SUM = ZERO"                )
    asm         (   LDB,    {0x41},     "COUNT = LENGTH OF ARRAY"   )
    asm         (   LDY,    0x42,       "POINT TO START OF ARRAY"   )
    asm  .SUMD  (   ADDA,   {0:Y+1},    "ADD NUMBER TO SUM"         )
    asm         (   DECB                                            )
    asm         (   BNE,    asm.SUMD                                )
    asm         (   STA,    {0x40}                                  )
    asm         (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '4F'
        'D6 41'
        '108E 0042'
        'AB A0'
        '5A'
        '26 FB'
        '97 40'
        '3F')


def test_levethal_5_2__16_bit_sum_of_data():
    asm = AsmDsl()
    asm         (   CLRA,               "MSB'S OF SUM = ZERO"       )
    asm         (   CLRB,               "LSB'S OF SUM = ZERO"       )
    asm         (   LDX,    0x43,       "POINT TO START OF ARRAY"   )
    asm  .SUMD  (   ADDB,   {0:X+1},    "SUM = SUM + DATA"          )
    asm         (   ADCA,   0,          "     AND ADD IN CARRY"     )
    asm         (   DEC,    {0x42},                                 )
    asm         (   BNE,    asm.SUMD                                )
    asm         (   STD,    {0x40},     "SAVE SUM"                  )
    asm         (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '4F'
        '5F'
        '8E 0043'
        'EB 80'
        '89 00'
        '0A 42'
        '26 F8'
        'DD 40'
        '3F')


def test_levethal_5_2__16_bit_sum_of_data_long_offset():
    asm = AsmDsl()
    asm         (   CLRA,               "MSB'S OF SUM = ZERO"       )
    asm         (   CLRB,               "LSB'S OF SUM = ZERO"       )
    asm         (   LDX,    0x43,       "POINT TO START OF ARRAY"   )
    asm  .SUMD  (   ADDB,   {0:X+1},    "SUM = SUM + DATA"          )
    asm         (   ADCA,   0,          "     AND ADD IN CARRY"     )
    asm         (   DEC,    {0x42},                                 )
    asm         (   LBRA,   asm.TEST                                )
    asm  .TEST  (   LBNE,   asm.SUMD                                )
    asm         (   STD,    {0x40},     "SAVE SUM"                  )
    asm         (   SWI                                             )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '4F'
        '5F'
        '8E 0043'
        'EB 80'
        '89 00'
        '0A 42'
        '16 0000' # Check!
        '1026 FFF3' # Check!
        'DD 40'
        '3F')


def test_levethal_5_3__number_of_negative_elements():
    asm = AsmDsl()
    asm         (   LDX,    0x42,       "POINT TO FIRST NUMBER"         )
    asm         (   CLRB,               "NUMBER OF NEGATIVES = ZERO"    )
    asm .CHKNEG (   LDA,    {0:X+1},    "IS NEXT ELEMENT NEGATIVE"      )
    asm         (   BPL,    asm.CHCNT                                   )
    asm         (   INCB,               "YES, ADD 1 TO # OF NEGATIVES"  )
    asm .CHCNT  (   DEC,    {0x41}                                      )
    asm         (   BNE,    asm.CHKNEG                                  )
    asm         (   STB,    {0x40},     "SAVE NUMBER OF NEGATIVES"      )
    asm         (   SWI                                                 )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '8E 0042'
        '5F'
        'A6 80'
        '2A 01'
        '5C'
        '0A 41'
        '26 F7'
        'D7 40'
        '3F')


def test_leventhal_5_4__maximum_value():
    asm = AsmDsl()
    asm         (   LDB,    {0x41},     "COUNT = NUMBER OF ELEMENTS"            )
    asm         (   CLRA,               "MAX = (MINIMUM POSSIBLE)"              )
    asm         (   LDX,    0x42,       "POINT TO FIRST ENTRY"                  )
    asm   .MAXM (   CMPA,   {0:X+1},    "IS CURRENT ENTRY GREATER THAN MAX"     )
    asm         (   BHS,    asm.NOCHG                                           )
    asm         (   LDA,    {-1:X},     "YES, REPLACE MAX WITH CURRENT ENTRY"   )
    asm  .NOCHG (   DECB,                                                       )
    asm         (   BNE,    asm.MAXM,                                           )
    asm         (   STA,    {0x40},     "SAVE MAXIMUM"                          )
    asm         (   SWI                                                         )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        'D6 41'
        '4F'
        '8E 0042'
        'A1 80'
        '24 02'
        'A6 1F'
        '5A'
        '26 F7'
        '97 40'
        '3F')


INDEX_REGISTER_CODES = {
    X: 0b00000000,
    Y: 0b00100000,
    U: 0b01000000,
    S: 0b01100000}


@given(index_register=sampled_from(sorted(INDEX_REGISTERS)))
def test_index_with_accumulator_A_offset(index_register):
    asm = AsmDsl()
    asm         (   LDB,    {A:index_register},     "ACCUMULATOR A OFFSET FROM INDEX REGISTER"   )

    code = assemble(statements(asm))
    assert code[0] == bytes(
        (0xE6,
         0b10000110  | INDEX_REGISTER_CODES[index_register]))


@given(index_register=sampled_from(sorted(INDEX_REGISTERS)))
def test_index_with_accumulator_B_offset(index_register):
    asm = AsmDsl()
    asm         (   LDA,    {B:index_register},     "ACCUMULATOR B OFFSET FROM INDEX REGISTER"   )

    code = assemble(statements(asm))
    assert code[0] == bytes(
        (0xA6,
         0b10000101  | INDEX_REGISTER_CODES[index_register]))


@given(index_register=sampled_from(sorted(INDEX_REGISTERS)))
def test_index_with_accumulator_D_offset(index_register):
    asm = AsmDsl()
    asm         (   LDA,    {D:index_register},     "ACCUMULATOR D OFFSET FROM INDEX REGISTER"   )

    code = assemble(statements(asm))
    assert code[0] == bytes(
        (0xA6,
         0b10001011  | INDEX_REGISTER_CODES[index_register]))

@given(index_register=sampled_from(sorted(INDEX_REGISTERS)))
def test_index_with_accumulator_E_offset(index_register):
    asm = AsmDsl()
    asm         (   LDA,    {E:index_register},     "ACCUMULATOR E OFFSET FROM INDEX REGISTER"   )

    code = assemble(statements(asm))
    assert code[0] == bytes(
        (0xA6,
         0b10000111  | INDEX_REGISTER_CODES[index_register]))


@given(index_register=sampled_from(sorted(INDEX_REGISTERS)))
def test_index_with_accumulator_F_offset(index_register):
    asm = AsmDsl()
    asm         (   LDA,    {F:index_register},     "ACCUMULATOR F OFFSET FROM INDEX REGISTER"   )

    code = assemble(statements(asm))
    assert code[0] == bytes(
        (0xA6,
         0b10001010  | INDEX_REGISTER_CODES[index_register]))


@given(index_register=sampled_from(sorted(INDEX_REGISTERS)))
def test_index_with_accumulator_W_offset(index_register):
    asm = AsmDsl()
    asm         (   LDA,    {W:index_register},     "ACCUMULATOR W OFFSET FROM INDEX REGISTER"   )

    code = assemble(statements(asm))
    assert code[0] == bytes(
        (0xA6,
         0b10001110  | INDEX_REGISTER_CODES[index_register]))


@given(index_register=sampled_from(sorted(INDEX_REGISTERS)))
def test_index_with_zero_offset(index_register):
    asm = AsmDsl()
    asm         (   LDA,    {0:index_register},     "ZERO OFFSET FROM INDEX REGISTER"   )

    code = assemble(statements(asm))
    assert code[0] == bytes(
        (0xA6,
         0b10000100 | INDEX_REGISTER_CODES[index_register]))


@given(index_register=sampled_from(sorted(INDEX_REGISTERS)),
       offset=integers(min_value=-16, max_value=+15))
@example(index_register=X, offset=-16)
@example(index_register=X, offset=+15)
def test_index_with_five_bit_offset(index_register, offset):
    assume(offset != 0)
    asm = AsmDsl()
    asm(   LDA,    {offset:index_register}, "5-BIT OFFSET FROM INDEX REGISTER"   )

    code = assemble(statements(asm))
    assert code[0] == bytes(
        (0xA6,
         INDEX_REGISTER_CODES[index_register] | twos_complement(offset, 5)))


@given(index_register=sampled_from(sorted(INDEX_REGISTERS)),
       offset=one_of(integers(min_value=-128, max_value=-17),
                     integers(min_value=+16, max_value=+127)))
@example(index_register=X, offset=-128)
@example(index_register=X, offset=-17)
@example(index_register=X, offset=+16)
@example(index_register=X, offset=+127)
def test_index_with_eight_bit_offset(index_register, offset):
    asm = AsmDsl()
    asm(   LDA,    {offset:index_register},  "8-BIT OFFSET FROM INDEX REGISTER"   )

    code = assemble(statements(asm))
    assert code[0] == bytes(
        (0xA6,
         0b10001000 | INDEX_REGISTER_CODES[index_register],
         twos_complement(offset, 8)))


@given(index_register=sampled_from(sorted(INDEX_REGISTERS)),
       offset=one_of(integers(min_value=-32768, max_value=-129),
                     integers(min_value=+128, max_value=+32767)))
@example(index_register=X, offset=-32768)
@example(index_register=X, offset=-129)
@example(index_register=X, offset=+128)
@example(index_register=X, offset=+32767)
def test_index_with_sixteen_bit_offset(offset, index_register):
    asm = AsmDsl()
    asm(   LDA,    {offset:index_register},  "16-BIT OFFSET FROM INDEX REGISTER"   )

    code = assemble(statements(asm))
    assert code[0] == (bytes(
        (0xA6,
         0b10001001 | INDEX_REGISTER_CODES[index_register]))
        + twos_complement(offset, 16).to_bytes(
        length=2, byteorder='big', signed=False))


@given(index_register=sampled_from(sorted(INDEX_REGISTERS)),
       offset=one_of(integers(max_value=-32769),
                     integers(min_value=+32768)))
@example(index_register=X, offset=-32769)
@example(index_register=X, offset=+32768)
def test_index_with_illegal_offset(offset, index_register):
    assume(offset != 0)
    asm = AsmDsl()

    with raises(ValueError):
        asm(   LDA,    {offset:index_register},  "OUT-OF-RANGE OFFSET FROM X REGISTER"   )


def test_leventhal_6_1a__length_of_a_string_of_characters():
    asm = AsmDsl()
    asm         (   CLRB,               "STRING LENGTH = ZERO"          )
    asm         (   LDX,    U16(0x41),  "POINT TO START OF STRING"      )
    asm         (   LDA,    U8(0x0D),   "GET ASCII CARRIAGE RETURN "
                                             "(STRING TERMINATOR)"      )
    asm  .CHKCR (   CMPA,   {0:X+1},    "IS NEXT CHARACTER "
                                                  "A CARRIAGE RETURN?"  )
    asm         (   BEQ,    asm.DONE,   "YES, END OF STRING"            )
    asm         (   INCB,               "NO, ADD 1 TO STRING LENGTH"    )
    asm         (   BRA,    asm.CHKCR,                                  )
    asm  .DONE  (   STB,    {0x40},     "SAVE STRING LENGTH"            )
    asm         (   SWI                                                 )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '5F'
        '8E 0041'
        '86 0D'
        'A1 80'
        '27 03'
        '5C'
        '20 F9'
        'D7 40'
        '3F')


def test_leventhal_6_1b__length_of_a_string_of_characters():
    asm = AsmDsl()
    asm         (   LDB,    0xFF,       "STRING LENGTH = -1"            )
    asm         (   LDX,    0x41,       "POINT TO START OF STRING"      )
    asm         (   LDA,    0x0D,       "GET ASCII CARRIAGE RETURN "
                                             "(STRING TERMINATOR)"      )
    asm  .CHKCR (   INCB,               "ADD 1 TO STRING LENGTH"        )
    asm         (   CMPA,   {0:X+1},    "IS NEXT CHARACTER "
                                                  "A CARRIAGE RETURN?"  )
    asm         (   BNE,    asm.CHKCR,   "NO, KEEP CHECKING"            )
    asm  .DONE  (   STB,    {0x40},      "YES, SAVE STRING LENGTH"      )
    asm         (   SWI                                                 )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        'C6 FF'
        '8E 0041'
        '86 0D'
        '5C'
        'A1 80'
        '26 FB'
        'D7 40'
        '3F'
    )


def test_program_counter_label():
    asm = AsmDsl()
    asm     (   LDX, asm.pc,    "LOAD PROGRAM COUNTER AS IMMEDIATE INTO X"  )
    asm     (   LDY, asm.pc,    "LOAD PROGRAM COUNTER AS IMMEDIATE INTO Y"  )
    asm     (   LDS, asm.pc,    "LOAD PROGRAM COUNTER AS IMMEDIATE INTO S"  )
    asm     (   LDU, asm.pc,    "LOAD PROGRAM COUNTER AS IMMEDIATE INTO U"  )
    asm     (   SWI                                                         )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '8E 00 00'
        '108E 00 03'
        '10CE 00 07'
        'CE 00 0b'
        '3F'
    )


def test_jump_addressing_mode_label_extended():
    asm = AsmDsl()
    asm .BEGIN ( JMP, {asm.BEGIN}, "LOOP FOREVER" )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '7E 00 00'
    )


def test_jump_addressing_mode_extended():
    asm = AsmDsl()
    asm .BEGIN ( JMP, {U16(0xC000)}, "LOOP FOREVER" )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '7E C0 00'
    )


def test_jump_addressing_mode_direct():
    asm = AsmDsl()
    asm  ( JMP, {U8(0xC0)}, "Jump to an address on the direct page" )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '0E C0'
    )


def test_jump_addressing_mode_immediate_raises_error():
    asm = AsmDsl()

    with raises(TypeError):
        asm .BEGIN ( JMP, 0xC000, "ERROR!" )


def test_fdb_addressing_mode_label_extended():
    asm = AsmDsl()
    asm .BEGIN ( FDB, (asm.BEGIN,), "Assemble current address" )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '00 00'
    )


def test_leventhal_6_2__find_first_non_blank_character():
    asm = AsmDsl()
    asm         (   LDX,    0x42,       "POINT TO START OF STRING"       )
    asm         (   LDA,    0x20,       "GET ASCII SPACE FOR COMPARISON ")
    asm  .CHBLK (   CMPA,   {0:X+1},    "IS CHARACTER AN ASCII SPACE?"   )
    asm         (   BEQ,    asm.CHBLK,  "YES, KEEP EXAMINING CHARS"      )
    asm         (   LEAX,   {-1:X},     "NO, MOVE POINTER BACK ONE"      )
    asm         (   STX,    {0x40},     "SAVE ADDRESS OF FIRST"
                                              "NON-BLANK CHARACTER"      )
    asm         (   SWI                                                  )

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '8E 0042'
        '86 20'
        'A1 80'
        '27 FC'
        '30 1F'
        '9F 40'
        '3F'
    )


def test_unresolved_label_reports_error():
    asm = AsmDsl()
    asm         (   BEQ,    asm.CHBLK,  "YES, KEEP EXAMINING CHARS"      )
    with raises(TooManyPassesError) as exc_info:
        assemble(statements(asm))
    assert exc_info.value.unresolved_label_names == ["CHBLK"]


def test_warning_log_is_empty_when_no_warnings_emitted():
    asm = AsmDsl()
    asm         (   ADDB,   {0x20},  "ADD 0x20 TO ACCUMULATOR B"      )

    logger = logging.getLogger('test-logger')
    logger.setLevel(logging.WARN)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    handler = ListLogHandler()
    logger.addHandler(handler)
    assemble(statements(asm), logger=logger)
    assert len(handler.messages) == 0


def test_unreferenced_label_reports_error():
    asm = AsmDsl()
    asm .UNUSED (   ADDB,   {0x20},  "ADD 0x20 TO ACCUMULATOR B"      )

    logger = logging.getLogger('test-logger')
    logger.setLevel(logging.WARN)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    handler = ListLogHandler()
    logger.addHandler(handler)
    assemble(statements(asm), logger=logger)
    assert handler.messages[0] == 'Unreferenced label: UNUSED'
