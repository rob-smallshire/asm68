from asm68.registers import *
from asm68.mnemonics import EXG
from asm68.asmdsl import AsmDsl, statements
from asm68.assembler import assemble, InterRegisterError
from helpers.code import check_object_code
from pytest import raises


def test_exg_a_a():
    check_object_code('1E 88', EXG, (A, A))


def test_exg_a_b():
    check_object_code('1E 89', EXG, (A, B))


def test_exg_x_y():
    check_object_code('1E 12', EXG, (X, Y))


def test_exg_md_a_raises_inter_register_error():
    asm = AsmDsl()
    asm(EXG, (MD, A))
    with raises(InterRegisterError):
        assemble(statements(asm))


def test_exg_s_z_raises_inter_register_error():
    asm = AsmDsl()
    asm(EXG, (S, Q))
    with raises(InterRegisterError):
        assemble(statements(asm))