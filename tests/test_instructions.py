from asmdsl import AsmDsl, statements
from assembler import assemble
from mnemonics import ABX


def test_abx_inherent():
    asm = AsmDsl()
    asm         (   ABX)

    code = assemble(statements(asm))
    assert code[0] == bytes.fromhex(
        '3B'
    )