from string import ascii_uppercase, digits, ascii_lowercase

from hypothesis import given
from hypothesis.strategies import text, characters, composite
from pytest import raises

from asm68.mnemonics import Mnemonic
from tests.predicates import check_balanced

ASCII_UPPERCASE_AND_DIGITS = ascii_uppercase + digits
ASCII_LOWERCASE_AND_DIGITS = ascii_lowercase + digits

@composite
def mnemonics(draw, min_size=1):
    if min_size < 0:
        raise ValueError("mnemonics(min_size={}) is negative".format(min_size))
    a_size = min(min_size, 1)
    b_size = min_size - a_size
    a = draw(text(min_size=a_size, max_size=1, alphabet=ascii_uppercase))
    b = draw(text(min_size=b_size, alphabet=ASCII_UPPERCASE_AND_DIGITS))
    return a + b

def test_empty_mnemonic_raises_value_error():
    with raises(ValueError):
        Mnemonic('')

@given(m=text(min_size=1, alphabet=ASCII_LOWERCASE_AND_DIGITS))
def test_illegal_initial_character_raises_value_error(m):
    with raises(ValueError):
        Mnemonic(m)

@given(p=text(min_size=1, max_size=1, alphabet=ascii_uppercase),
       q=text(min_size=1, alphabet=ascii_lowercase))
def test_illegal_unicode_categories_raise_value_error(p, q):
    m = p + q
    with raises(ValueError):
        Mnemonic(m)

@given(m=mnemonics())
def test_mnemonic_value(m):
    assert str(Mnemonic(m)) == m

@given(m=mnemonics())
def test_mnemonic_interning(m):
    assert Mnemonic(m) is Mnemonic(m)

@given(m=mnemonics())
def test_mnemonic_repr(m):
    r = repr(Mnemonic(m))
    assert r.startswith('Mnemonic')
    assert m in r
    assert check_balanced(r)