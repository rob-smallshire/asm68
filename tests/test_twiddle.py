import sys
from hypothesis import given
from hypothesis.strategies import integers
from math import log, floor

from pytest import raises

from asm68.twiddle import twos_complement

@given(num_bits=integers(max_value=0))
def test_twos_complement_non_positive_num_bits_raises_value_error(num_bits):
    with raises(ValueError):
        twos_complement(0, num_bits)

@given(n=integers(min_value=1))
def test_twos_complement_positive(n):
    assert twos_complement(n, 2 + floor(log(n)/log(2))) == n

@given(n=integers(min_value=1))
def test_twos_complement_too_narrow(n):
    with raises(ValueError):
        assert twos_complement(n, 1)

@given(n=integers(min_value=-128, max_value=-1))
def test_twos_complement_negative(n):
    assert twos_complement(n, 8) == 256 + n