from asm68.registers import *
from asm68.mnemonics import TFR
from asm68.asmdsl import AsmDsl, statements
from asm68.assembler import assemble, InterRegisterError
from helpers import check_object_code
from pytest import raises


def test_tfr_a_a():
    check_object_code('1F 88', TFR, (A, A))


def test_tfr_a_b():
    check_object_code('1F 89', TFR, (A, B))


def test_tfr_x_y():
    check_object_code('1F 12', TFR, (X, Y))


def test_tfr_md_a_raises_inter_register_error():
    asm = AsmDsl()
    asm(TFR, (MD, A))
    with raises(InterRegisterError):
        assemble(statements(asm))


def test_tfr_s_z_raises_inter_register_error():
    asm = AsmDsl()
    asm(TFR, (S, Q))
    with raises(InterRegisterError):
        assemble(statements(asm))