import gc
from hypothesis import given, assume
from hypothesis.strategies import lists, integers
from pytest import raises

from asm68.addrmodes import Immediate, Inherent, PageDirect, ExtendedDirect, ExtendedIndirect, Registers, Indexed
from asm68.asmdsl import AsmDsl, statements, statement_index, parse_operand
from asm68.ast import MNEMONIC_TO_AST
from asm68.instructions import Abx, Lda, Adda, Addb, Inc, Tfr, Pshs, LDB, SUBA, CMPA, BLO, STB, SWI
from asm68.label import Label
from asm68.mnemonics import ABX, LDA, ADDB, ADDA, INC, ASLA, ASRA, LSRA, TFR, PSHS, Mnemonic
from asm68.registers import A, B, PC, U, Y, X, DP, CC
from tests.test_mnemonics import mnemonics


def test_none_returns_inherent_addressing_mode():
    operand = None
    r = parse_operand(operand)
    assert isinstance(r, Inherent)

def test_bare_integer_returns_immediate_addressing_mode():
    operand = 0x30
    r = parse_operand(operand)
    assert isinstance(r, Immediate)

def test_value_stored_in_immediate_addressing_mode():
    operand = 0x42
    r = parse_operand(operand)
    assert r.value == operand

def test_set_with_one_byte_value_returns_page_direct_addressing_mode():
    operand = {0x30}
    r = parse_operand(operand)
    assert isinstance(r, PageDirect)

def test_address_stored_in_page_direct_addressing_mode():
    address = 0x78
    operand = {address}
    r = parse_operand(operand)
    assert r.address == address

def test_set_with_negative_address_raises_value_error():
    operand = {-1}
    with raises(ValueError):
        parse_operand(operand)

def test_empty_set_raises_value_error():
    operand = set()
    with raises(ValueError):
        parse_operand(operand)

def test_set_with_multiple_items_raises_value_error():
    operand = {0x1C, 0xD5}
    with raises(ValueError):
        parse_operand(operand)

def test_set_with_two_byte_value_returns_extended_direct_addressing_mode():
    operand = {0x1C48}
    r = parse_operand(operand)
    assert isinstance(r, ExtendedDirect)

def test_address_stored_in_extended_direct_addressing_mode():
    address = 0xD58A
    operand = {address}
    r = parse_operand(operand)
    assert r.address == address

def test_set_with_three_byte_value_raises_value_error():
    address = 0x010000
    operand = {address}
    with raises(ValueError):
        parse_operand(operand)

def test_set_with_label_returns_extended_direct_addressing_mode():
    address = Label('loop')
    operand = {address}
    r = parse_operand(operand)
    assert r.address == address

def test_set_with_string_raises_type_error():
    address = 'hello'
    operand = {address}
    with raises(TypeError):
        parse_operand(operand)

def test_list_causes_indirection_for_integer_address():
    address = 0x3560
    operand = [{address}]
    r = parse_operand(operand)
    assert isinstance(r, ExtendedIndirect)

def test_list_causes_indirection_for_label():
    address = Label('loop')
    operand = [{address}]
    r = parse_operand(operand)
    assert isinstance(r, ExtendedIndirect)

# TODO: Indexed addressing

def test_inherent_address_assembly():
    asm = AsmDsl()
    asm( ABX )
    assert statements(asm) == (Abx(Inherent()), )

def test_register_two_address_assembly():
    asm = AsmDsl()
    asm( TFR, (A, B) )
    assert statements(asm) == (Tfr(Registers((A, B))), )

def test_register_seven_address_assembly():
    asm = AsmDsl()
    asm( PSHS, (PC, U, Y, X, DP, B, A, CC) )
    assert statements(asm) == (Pshs(Registers((PC, U, Y, X, DP, B, A, CC))), )

def test_immediate_address_assembly():
    asm = AsmDsl()
    asm( LDA, 0x30 )
    assert statements(asm) == (Lda(Immediate(0x30)),)

def test_page_direct_address_assembly():
    asm = AsmDsl()
    asm( ADDA, {0x30} )
    assert statements(asm) == (Adda(PageDirect(0x30)), )

def test_extended_direct_address_assembly():
    asm = AsmDsl()
    asm( ADDB, {0x1C48} )
    assert statements(asm) == (Addb(ExtendedDirect(0x1C48)), )

def test_extended_indirect_address_assembly():
    asm = AsmDsl()
    asm( INC, [{0x1C48}] )
    assert statements(asm) == (Inc(ExtendedIndirect(0x1C48)), )

def test_incorrect_inherent_addressing_mode_raises_type_error():
    asm = AsmDsl()
    with raises(TypeError):
        asm( INC )

def test_incorrect_immediate_addressing_mode_raises_type_error():
    asm = AsmDsl()
    with raises(TypeError):
        asm( ASLA, 0x42 )

def test_incorrect_direct_addressing_mode_raises_type_error():
    asm = AsmDsl()
    with raises(TypeError):
        asm( ASRA, {0x42} )

def test_incorrect_extended_addressing_mode_raises_type_error():
    asm = AsmDsl()
    with raises(TypeError):
        asm( LSRA, {0x4242} )

def test_indexed_zero_offset():
    asm = AsmDsl()
    asm( ADDA, {0: X} )
    assert statements(asm) == (Adda(Indexed(X, 0)), )

def test_make_label():
    asm = AsmDsl()
    asm  .loop  ( ADDA, 0x30 )
    assert statement_index(asm, 'loop') == 0

def test_refer_to_label():
    asm = AsmDsl()
    asm  .loop  ( ADDA, 0x30 )
    assert asm.loop == Label('loop')

@given(args=lists(min_size=4, elements=integers()))
def test_incorrect_number_of_arguments(args):
    asm = AsmDsl()
    with raises(TypeError):
        asm(*args)

@given(m=mnemonics())
def test_unknown_mnemonic_raises_value_error(m):
    mnemonic = Mnemonic(m)
    assume(mnemonic not in MNEMONIC_TO_AST)
    asm = AsmDsl()
    with raises(ValueError):
        asm(mnemonic)

def test_garbage_collected_dsl_raises_runtime_error():
    mnemonic = Mnemonic('FOO')
    asm = AsmDsl()
    labeller = asm.label
    del asm
    gc.collect()
    with raises(RuntimeError):
        labeller(mnemonic)

def test_parse_operand_unsupported_type_raises_not_implemented_error():
    FOO = Mnemonic('FOO')
    asm = AsmDsl()
    with raises(TypeError):
        asm(FOO, object())

def test_parse_operand_unsupported_indirect_type_raises_not_implemented_error():
    FOO = Mnemonic('FOO')
    asm = AsmDsl()
    with raises(TypeError):
        asm(FOO, [object()])

@given(address=integers(max_value=-1))
def test_negative_indirect_address_raises_value_error(address):
    FOO = Mnemonic('FOO')
    asm = AsmDsl()
    with raises(ValueError):
        asm(FOO, {address})
