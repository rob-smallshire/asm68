from asm68.asmdsl import AsmDsl, statements
from asm68.assembler import assemble
from asm68.mnemonics import ABX


def test_abx_inherent():
    asm = AsmDsl()
    asm         (   ABX)

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '3A'
    )
