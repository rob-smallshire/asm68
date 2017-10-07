from asm68.addrmodes import Immediate, Inherent, PageDirect, ExtendedDirect, ExtendedIndirect
from asm68.asmdsl import AsmDsl
from asm68.ast import Abx, Lda, Adda, Addb, Inc
from asm68.mnemonics import ABX, LDA, ADDB, ADDA, INC


def test_inherent_address_assembly():
    asm = AsmDsl()
    asm( ABX )
    assert asm.statements == (Abx(Inherent()), )


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

