from asm68.asmdsl import AsmDsl, statements
from asm68.assembler import assemble
from asm68.registers import *
from asm68.mnemonics import *


def test_abx_inherent():
    asm = AsmDsl()
    asm         (   ABX)

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '3A'
    )

def test_adc_immediate():
    asm = AsmDsl()
    asm (ADCA, 0x34)
    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '89 34'
    )


def test_adc_direct():
    asm = AsmDsl()
    asm (ADCA, {0x34})
    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '99 34'
    )

def test_adc_indexed():
    asm = AsmDsl()
    asm (ADCA, {0:X})
    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        'A9 84'
    )

def test_extended_direct():
    asm = AsmDsl()
    asm (ADCA, {0x1234})
    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        'B9 12 34'
    )
