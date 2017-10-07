from pytest import raises

from asm68.addrmodes import Immediate, Inherent, PageDirect, ExtendedDirect, ExtendedIndirect, Registers
from asm68.asmdsl import AsmDsl
from asm68.ast import Abx, Lda, Adda, Addb, Inc, Tfr, Pshs
from asm68.mnemonics import ABX, LDA, ADDB, ADDA, INC, ASLA, ASRA, LSRA, TFR, PSHS
from asm68.registers import A, B, PC, U, Y, X, DP, CC


def test_inherent_address_assembly():
    asm = AsmDsl()
    asm( ABX )
    assert asm.statements == (Abx(Inherent()), )

def test_register_two_address_assembly():
    asm = AsmDsl()
    asm( TFR, (A, B) )
    assert asm.statements == (Tfr(Registers((A, B))), )

def test_register_seven_address_assembly():
    asm = AsmDsl()
    asm( PSHS, (PC, U, Y, X, DP, B, A, CC) )
    assert asm.statements == (Pshs(Registers((PC, U, Y, X, DP, B, A, CC))), )

def test_immediate_address_assembly():
    asm = AsmDsl()
    asm( LDA, 0x30 )
    assert asm.statements == (Lda(Immediate(0x30)), )


def test_page_direct_address_assembly():
    asm = AsmDsl()
    asm( ADDA, {0x30} )
    assert asm.statements == (Adda(PageDirect(0x30)), )

def test_extended_direct_address_assembly():
    asm = AsmDsl()
    asm( ADDB, {0x1C48} )
    assert asm.statements == (Addb(ExtendedDirect(0x1C48)), )

def test_extended_indirect_address_assembly():
    asm = AsmDsl()
    asm( INC, [{0x1C48}] )
    assert asm.statements == (Inc(ExtendedIndirect(0x1C48)), )

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

# def leventhal_example_program_7_3():
#     asm = AsmDsl()
#     asm     (   LDB,    0xFF,       "GET ERROR MARKER"          )
#     asm     (   LDA,    {0x40},     "GET DATA"                  )
#     asm     (   SUBA,   '0',        "IS DATA BELOW ASCII ZERO?" )
#     asm     (   BLO,    asm.done,   "    YES, NOT A DIGIT"      )
#     asm     (   CMPA,   '9',        "IS DATA ABOVE ASCII NINE?" )
#     asm     (   TFR,    A,B)