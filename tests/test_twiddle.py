from hypothesis import given, assume
from hypothesis.strategies import integers, data

from pytest import raises

from asm68.twiddle import twos_complement

@given(num_bits=integers(max_value=0))
def test_twos_complement_non_positive_num_bits_raises_value_error(num_bits):
    with raises(ValueError):
        twos_complement(0, num_bits)

@given(data())
def test_twos_complement_positive(d):
    num_bits = d.draw(integers(min_value=1))
    value = d.draw(integers(min_value=0, max_value=(2**(num_bits-1)) - 1))
    assert twos_complement(value, num_bits) == value


@given(d=data())
def test_twos_complement_negative(d):
    num_bits = d.draw(integers(min_value=1))
    value = d.draw(integers(min_value=-2**(num_bits-1), max_value=-1))
    c = int(''.join(str(int(not int(x))) for x in bin(abs(value) - 1)[2:]).rjust(num_bits, '1'), 2)
    assert twos_complement(value, num_bits) == c


@given(d=data())
def test_twos_complement_positive_too_narrow(d):
    value = d.draw(integers(min_value=0))
    num_bits = d.draw(integers(min_value=0, max_value=value.bit_length()))
    assume(num_bits >= 1)
    with raises(ValueError):
        twos_complement(value, num_bits)

def test_twos_complement_minus_one_too_narrow():
    with raises(ValueError):
        twos_complement(-1, 0)

@given(d=data())
def test_twos_complement_negative_too_narrow(d):
    value = d.draw(integers(max_value=-2))
    num_bits = d.draw(integers(min_value=1, max_value=value.bit_length() - 1))
    with raises(ValueError):
        twos_complement(value, num_bits)

