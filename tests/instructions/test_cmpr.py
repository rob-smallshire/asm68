from asm68.registers import *
from asm68.mnemonics import CMPR
from asm68.asmdsl import AsmDsl, statements
from asm68.assembler import assemble, InterRegisterError
from helpers import check_object_code
from pytest import raises


def test_cmpr_a_a():
    check_object_code('10 37 88', CMPR, (A, A))


def test_cmpr_a_b():
    check_object_code('10 37 89', CMPR, (A, B))


def test_cmpr_x_y():
    check_object_code('10 37 12', CMPR, (X, Y))


def test_cmpr_md_a_raises_inter_register_error():
    asm = AsmDsl()
    asm(CMPR, (MD, A))
    with raises(InterRegisterError):
        assemble(statements(asm))


def test_cmpr_s_z_raises_inter_register_error():
    asm = AsmDsl()
    asm(CMPR, (S, Q))
    with raises(InterRegisterError):
        assemble(statements(asm))