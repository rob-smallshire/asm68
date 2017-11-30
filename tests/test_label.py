from hypothesis import given, assume
from hypothesis.strategies import from_regex, composite, text
from pytest import raises

from asm68.label import Label
from asm68.util import is_valid_variable_name
from tests.predicates import check_balanced


@composite
def label_names(draw):
    label_name = draw(from_regex(r'\A[A-Za-z][A-Za-z0-9_]*\Z'))
    assume(is_valid_variable_name(label_name))
    return label_name

@given(name=label_names())
def test_label_value(name):
    assume(is_valid_variable_name(name))
    assert Label(name).name == name

@given(name=text())
def test_illegal_label_name_raises_value_error(name):
    assume(not is_valid_variable_name(name))
    with raises(ValueError):
        Label(name)

@given(name=label_names())
def test_label_repr(name):
    assume(is_valid_variable_name(name))
    r = repr(Label(name))
    assert r.startswith('Label')
    assert name in r
    assert check_balanced(r)

@given(name=label_names())
def test_label_equality(name):
    assume(is_valid_variable_name(name))
    assert Label(name) == Label(name)

@given(name=label_names())
def test_label_hash_equality(name):
    assume(is_valid_variable_name(name))
    assert hash(Label(name)) == hash(Label(name))

@given(name=label_names())
def test_label_equality_differing_type(name):
    assume(is_valid_variable_name(name))
    assert Label(name) != object()

@given(name_a=label_names(),
       name_b=label_names())
def test_label_inequality(name_a, name_b):
    assume(name_a != name_b)
    assert Label(name_a) != Label(name_b)

