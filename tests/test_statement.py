from hypothesis import given, assume, settings
from hypothesis.strategies import composite, integers, text
from pytest import raises

from asm68.label import Label
from asm68.statement import Statement
from asm68.util import is_valid_variable_name
from tests.predicates import check_balanced
from tests.test_label import label_names
from tests.test_mnemonics import mnemonics

@composite
def statement_classes(draw):
    m = draw(mnemonics(min_size=1))
    cls_name = m.title()
    return type(cls_name,
                (Statement,),
                {'mnemonic': m})

def test_intantiating_abstract_statement_raises_value_error():
    class Foo(Statement):
        pass
    with raises(NotImplementedError):
        Foo(None)

@given(cls=statement_classes(),
       operand=integers(0x00, 0xFF),
       comment=text(),
       label_name=label_names())
def test_instantiating_concrete_statement(cls, operand, comment, label_name):
    assume(is_valid_variable_name(label_name))
    label = Label(label_name)
    s = cls(operand, comment, label)
    assert s.operand == operand
    assert s.comment == comment
    assert s.label == label

@given(cls=statement_classes(),
       operand=integers(0x00, 0xFF),
       comment=text(),
       label_name=label_names())
def test_statement_equality(cls, operand, comment, label_name):
    assume(is_valid_variable_name(label_name))
    assert cls(operand, comment, Label(label_name)) == cls(operand, comment, Label(label_name))

@given(cls=statement_classes(),
       operand=integers(0x00, 0xFF),
       comment=text(),
       label_name=label_names())
def test_statement_hash_equality(cls, operand, comment, label_name):
    assume(is_valid_variable_name(label_name))
    assert hash(cls(operand, comment, Label(label_name))) == hash(cls(operand, comment, Label(label_name)))

@given(cls=statement_classes(),
       operand=integers(0x00, 0xFF),
       comment=text(),
       label_name=label_names())
def test_statement_inequality_different_type(cls, operand, comment, label_name):
    assume(is_valid_variable_name(label_name))
    assert cls(operand, comment, Label(label_name)) != object()

@given(cls=statement_classes(),
       operand_a=integers(0x00, 0xFF),
       comment_a=text(),
       label_name_a=label_names(),
       operand_b=integers(0x00, 0xFF),
       comment_b=text(),
       label_name_b=label_names())
def test_statement_equality(cls, operand_a, comment_a, label_name_a, operand_b, comment_b, label_name_b):
    assume(is_valid_variable_name(label_name_a))
    assume(is_valid_variable_name(label_name_b))
    assume((operand_a != operand_b) or (comment_a != comment_b) or (label_name_a != label_name_b))
    assert cls(operand_a, comment_a, Label(label_name_a)) != cls(operand_b, comment_b, Label(label_name_b))

@given(cls=statement_classes(),
       operand=integers(0x00, 0xFF),
       comment=text(),
       label_name=label_names())
def test_label_repr(cls, operand, comment, label_name):
    assume(is_valid_variable_name(label_name))
    label = Label(label_name)
    r = repr(cls(operand, comment, label))
    assert r.startswith(cls.__name__)
    assert repr(operand) in r
    assert repr(label) in r
    assert check_balanced(r)
