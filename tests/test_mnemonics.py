from hypothesis import given
from hypothesis.strategies import text
from pytest import raises

from asm68.mnemonics import Mnemonic
from helpers.alphabets import DIGITS
from helpers.predicates import check_balanced
from helpers.strategies import mnemonics


def test_empty_mnemonic_raises_value_error():
    with raises(ValueError):
        Mnemonic('')

@given(m=text(min_size=1, alphabet=DIGITS))
def test_mnemonic_illegal_initial_character_raises_value_error(m):
    with raises(ValueError):
        Mnemonic(m)

@given(m=mnemonics())
def test_mnemonic_value(m):
    assert str(Mnemonic(m)) == m

@given(m=mnemonics())
def test_mnemonic_repr(m):
    r = repr(Mnemonic(m))
    assert r.startswith('Mnemonic')
    assert m in r
    assert check_balanced(r)

