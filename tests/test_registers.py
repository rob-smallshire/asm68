from string import ascii_uppercase

from hypothesis import given, assume
from hypothesis.strategies import text, integers
from pytest import raises

from asm6x.registers import Register, REGISTERS
from tests.alphabets import ASCII_LOWERCASE_AND_DIGITS
from tests.predicates import check_balanced

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_interning(m):
    Register._instances.clear()
    assert Register(m, len(m)) is Register(m, len(m))

def test_empty_register_raises_value_error():
    Register._instances.clear()
    with raises(ValueError):
        Register('', 1)

@given(m=text(min_size=1, alphabet=ASCII_LOWERCASE_AND_DIGITS))
def test_register_illegal_initial_character_raises_value_error(m):
    Register._instances.clear()
    with raises(ValueError):
        Register(m, len(m))

@given(name=text(min_size=1, alphabet=ascii_uppercase))
def test_register_name(name):
    Register._instances.clear()
    assume(name not in {r.name for r in REGISTERS})
    assert str(Register(name, len(name))) == name

@given(name=text(min_size=1, alphabet=ascii_uppercase),
       width_a=integers(min_value=1),
       width_b=integers(min_value=1))
def test_inconsistent_width_raises_value_error(name, width_a, width_b):
    assume(width_a != width_b)
    Register._instances.clear()
    Register(name, width_a)
    with raises(ValueError):
        Register(name, width_b)

def test_register_width():
    Register._instances.clear()
    assert Register('FOO', 2).width == 2

@given(width=integers(max_value=0))
def test_illegal_register_width(width):
    Register._instances.clear()
    with raises(ValueError):
        Register('BAR', width)

@given(name=text(min_size=4, alphabet=ascii_uppercase))
def test_register_unspecified_width_raises_value_error(name):
    Register._instances.clear()
    with raises(ValueError):
        Register(name)

@given(name=text(min_size=4, alphabet=ascii_uppercase))
def test_register_repr(name):
    Register._instances.clear()
    r = repr(Register(name, len(name)))
    assert r.startswith('Register')
    assert name in r
    assert str(len(name)) in r
    assert check_balanced(r)

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_equality(m):
    Register._instances.clear()
    assert Register(m, len(m)) == Register(m, len(m))

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       n=text(min_size=1, alphabet=ascii_uppercase))
def test_register_inequality(m, n):
    Register._instances.clear()
    assume(m != n)
    assert Register(m, len(m)) != Register(n, len(n))

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_inequality_different_types(m):
    Register._instances.clear()
    assert Register(m, len(m)) != object()

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_hash_equality(m):
    Register._instances.clear()
    assert hash(Register(m, len(m))) == hash(Register(m, len(m)))

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_less_than_different_types(m):
    Register._instances.clear()
    with raises(TypeError):
        assert Register(m, len(m)) < object()