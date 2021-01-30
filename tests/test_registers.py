from string import ascii_uppercase

from hypothesis import given, assume
from hypothesis.strategies import text, integers, one_of, just
from pytest import raises

from asm68.registers import Register, REGISTERS, AutoIncrementedRegister, ACCUMULATORS, A, B, E, F, \
    D, W, Q, X, Y, U, S, \
    INDEX_REGISTERS, DP, CC, MD, PC, STATUS_REGISTERS, V, Z
from tests.alphabets import ASCII_LOWERCASE_AND_DIGITS
from tests.predicates import check_balanced

def test_empty_register_raises_value_error():
    with raises(ValueError):
        Register('', 1)

@given(m=text(min_size=1, alphabet=ASCII_LOWERCASE_AND_DIGITS))
def test_register_illegal_initial_character_raises_value_error(m):
    with raises(ValueError):
        Register(m, len(m))

@given(name=text(min_size=1, alphabet=ascii_uppercase))
def test_register_name(name):
    assume(name not in {r.name for r in REGISTERS})
    assert str(Register(name, len(name))) == name

@given(name=text(min_size=1, alphabet=ascii_uppercase),
       width_a=integers(min_value=1),
       width_b=integers(min_value=1))
def test_inconsistent_width_raises_value_error(name, width_a, width_b):
    Register._names_and_widths.clear()
    assume(width_a != width_b)
    Register(name, width_a)
    with raises(ValueError):
        Register(name, width_b)

def test_register_width():
    Register._names_and_widths.clear()
    assert Register('FOO', 2).width == 2

def test_register_width_default():
    Register._names_and_widths.clear()
    Register('FOO', 2)
    assert Register('FOO').width == 2

@given(width=integers(max_value=0))
def test_illegal_register_width(width):
    with raises(ValueError):
        Register('BAR', width)

@given(name=text(min_size=4, alphabet=ascii_uppercase))
def test_register_unspecified_width_raises_value_error(name):
    with raises(ValueError):
        Register(name)

@given(name=text(min_size=4, alphabet=ascii_uppercase))
def test_register_repr(name):
    r = repr(Register(name, len(name)))
    assert r.startswith('Register')
    assert name in r
    assert str(len(name)) in r
    assert check_balanced(r)

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_equality(m):
    Register._names_and_widths.clear()
    assert Register(m, len(m)) == Register(m, len(m))

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       n=text(min_size=1, alphabet=ascii_uppercase))
def test_register_inequality(m, n):
    Register._names_and_widths.clear()
    assume(m != n)
    assert Register(m, len(m)) != Register(n, len(n))

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_inequality_different_types(m):
    Register._names_and_widths.clear()
    assert Register(m, len(m)) != object()

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_hash_equality(m):
    Register._names_and_widths.clear()
    assert hash(Register(m, len(m))) == hash(Register(m, len(m)))

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_less_than_different_types(m):
    Register._names_and_widths.clear()
    with raises(TypeError):
        assert Register(m, len(m)) < object()

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       delta=one_of(just(-2), just(-1), just(+1), just(+2)))
def test_register_post_increment(m, delta):
    Register._names_and_widths.clear()
    r = Register(m, len(m))
    assert r+delta == AutoIncrementedRegister(r, delta)

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       delta=one_of(just(-2), just(-1), just(+1), just(+2)))
def test_register_pre_decrement(m, delta):
    Register._names_and_widths.clear()
    r = Register(m, len(m))
    assert delta-r == AutoIncrementedRegister(r, -delta)

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       delta=integers())
def test_register_post_increment_with_illegal_delta_raises_value_error(m, delta):
    assume(delta not in {-2, -1, +1, +2})
    Register._names_and_widths.clear()
    r = Register(m, len(m))
    with raises(ValueError):
        r+delta

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       delta=integers())
def test_register_pre_decrement_with_illegal_delta_raises_value_error(m, delta):
    assume(delta not in {-2, -1, +1, +2})
    Register._names_and_widths.clear()
    r = Register(m, len(m))
    with raises(ValueError):
       delta-r

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_post_increment_with_illegal_delta_raises_type_error(m):
    Register._names_and_widths.clear()
    r = Register(m, len(m))
    with raises(TypeError):
        r+object()

@given(m=text(min_size=1, alphabet=ascii_uppercase))
def test_register_pre_decrement_with_illegal_delta_raises_type_error(m):
    Register._names_and_widths.clear()
    r = Register(m, len(m))
    with raises(TypeError):
       object()-r

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       delta=integers())
def test_auto_incremented_register_increments_out_of_range_raise_value_error(m, delta):
    assume(delta not in {-2, -1, +1, +2})
    Register._names_and_widths.clear()
    r = Register(m, len(m))
    with raises(ValueError):
        AutoIncrementedRegister(r, delta)

@given(name=text(min_size=4, alphabet=ascii_uppercase),
       delta=one_of(just(-2), just(-1), just(+1), just(+2)))
def test_auto_incremented_register_repr(name, delta):
    a = Register(name, len(name))
    r = repr(AutoIncrementedRegister(a, delta))
    assert r.startswith('AutoIncrementedRegister')
    assert name in r
    assert str(delta) in r
    assert check_balanced(r)

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       delta=one_of(just(-2), just(-1), just(+1), just(+2)))
def test_auto_incremented_register_equality(m, delta):
    Register._names_and_widths.clear()
    a = Register(m, len(m))
    b = Register(m, len(m))
    assert AutoIncrementedRegister(a, delta) == AutoIncrementedRegister(b, delta)

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       delta=one_of(just(-2), just(-1), just(+1), just(+2)))
def test_auto_incremented_register_inequality_different_types(m, delta):
    Register._names_and_widths.clear()
    a = Register(m, len(m))
    assert AutoIncrementedRegister(a, delta) != object()

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       n=text(min_size=1, alphabet=ascii_uppercase),
       delta=one_of(just(-2), just(-1), just(+1), just(+2)),
       gamma=one_of(just(-2), just(-1), just(+1), just(+2)))
def test_auto_incremented_register_inequality(m, n, delta, gamma):
    assume((m != n) or (delta != gamma))
    Register._names_and_widths.clear()
    a = Register(m, len(m))
    b = Register(n, len(n))
    assert AutoIncrementedRegister(a, delta) != AutoIncrementedRegister(b, gamma)

@given(m=text(min_size=1, alphabet=ascii_uppercase),
       delta=one_of(just(-2), just(-1), just(+1), just(+2)))
def test_auto_incremented_register_hash_equality(m, delta):
    Register._names_and_widths.clear()
    a = Register(m, len(m))
    b = Register(m, len(m))
    assert hash(AutoIncrementedRegister(a, delta)) == hash(AutoIncrementedRegister(b, delta))

def test_6309_accumulators_register_set():
    assert ACCUMULATORS == {A, B, E, F, D, W, Q}

def test_6309_index_register_set():
    assert INDEX_REGISTERS == {X, Y, U, S}

def test_6309_status_register_set():
    assert STATUS_REGISTERS == {DP, CC, MD, PC}

def test_6309_register_set():
    assert REGISTERS == {X, Y, U, S, A, B, E, F, D, W, Q, DP, CC, MD, PC, V, Z}

