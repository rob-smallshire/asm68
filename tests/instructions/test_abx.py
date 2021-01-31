from asm68.mnemonics import ABX
from helpers import check_object_code


def test_abx_inherent():
    check_object_code("3A", ABX)
