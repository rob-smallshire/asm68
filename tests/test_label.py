from hypothesis import given, assume, settings
from hypothesis.strategies import text, fractions
from pytest import raises

from asm68.label import Label
from tests.predicates import is_valid_variable_name, check_balanced


@given(name=text(min_size=1))
def test_label_value(name):
    assume(is_valid_variable_name(name))
    assert Label(name).name == name

@given(name=text())
def test_illegal_label_name_raises_value_error(name):
    assume(not is_valid_variable_name(name))
    with raises(ValueError):
        Label(name)

@given(name=text(min_size=1))
def test_label_repr(name):
    assume(is_valid_variable_name(name))
    r = repr(Label(name))
    assert r.startswith('Label')
    assert name in r
    assert check_balanced(r)

@given(name=text(min_size=1))
def test_label_equality(name):
    assume(is_valid_variable_name(name))
    assert Label(name) == Label(name)

@given(name=text(min_size=1))
def test_label_hash_equality(name):
    assume(is_valid_variable_name(name))
    assert hash(Label(name)) == hash(Label(name))

@given(name=text(min_size=1))
def test_label_equality_differing_type(name):
    assume(is_valid_variable_name(name))
    assert Label(name) != object()

@given(name_a=text(min_size=1),
       name_b=text(min_size=1))
@settings(max_examples=2000)
def test_label_inequality(name_a, name_b):
    assume(is_valid_variable_name(name_a))
    assume(is_valid_variable_name(name_b))
    assume(name_a != name_b)
    assert Label(name_a) != Label(name_b)

