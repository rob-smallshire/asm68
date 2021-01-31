from asm68.registers import *
from asm68.mnemonics import ADCA
from helpers import check_object_code


def test_adc_immediate():
    check_object_code('89 34', ADCA, 0x34)


def test_adc_direct():
    check_object_code('99 34', ADCA, {0x34})


def test_adc_indexed():
    check_object_code('A9 84', ADCA, {0:X})


def test_extended_direct():
    check_object_code('B9 12 34', ADCA, {0x1234})
