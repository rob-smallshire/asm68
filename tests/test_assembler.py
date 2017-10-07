from pytest import raises

from asm68.asmdsl import parse_operand
from asm68.label import Label
from asm68.addrmodes import Immediate, Inherent, PageDirect, ExtendedDirect, ExtendedIndirect


def test_none_returns_inherent_addressing_mode():
    operand = None
    r = parse_operand(operand)
    assert isinstance(r, Inherent)

def test_bare_integer_returns_immediate_addressing_mode():
    operand = 0x30
    r = parse_operand(operand)
    assert isinstance(r, Immediate)

def test_value_stored_in_immediate_addressing_mode():
    operand = 0x42
    r = parse_operand(operand)
    assert r.value == operand

def test_set_with_one_byte_value_returns_page_direct_addressing_mode():
    operand = {0x30}
    r = parse_operand(operand)
    assert isinstance(r, PageDirect)

def test_address_stored_in_page_direct_addressing_mode():
    address = 0x78
    operand = {address}
    r = parse_operand(operand)
    assert r.address == address

def test_set_with_negative_address_raises_value_error():
    operand = {-1}
    with raises(ValueError):
        parse_operand(operand)

def test_empty_set_raises_value_error():
    operand = set()
    with raises(ValueError):
        parse_operand(operand)

def test_set_with_multiple_items_raises_value_error():
    operand = {0x1C, 0xD5}
    with raises(ValueError):
        parse_operand(operand)

def test_set_with_two_byte_value_returns_extended_direct_addressing_mode():
    operand = {0x1C48}
    r = parse_operand(operand)
    assert isinstance(r, ExtendedDirect)

def test_address_stored_in_extended_direct_addressing_mode():
    address = 0xD58A
    operand = {address}
    r = parse_operand(operand)
    assert r.address == address

def test_set_with_three_byte_value_raises_value_error():
    address = 0x010000
    operand = {address}
    with raises(ValueError):
        parse_operand(operand)

def test_set_with_label_returns_extended_direct_addressing_mode():
    address = Label('loop')
    operand = {address}
    r = parse_operand(operand)
    assert r.address == address

def test_set_with_string_raises_type_error():
    address = 'hello'
    operand = {address}
    with raises(TypeError):
        parse_operand(operand)

def test_list_causes_indirection_for_integer_address():
    address = 0x3560
    operand = [{address}]
    r = parse_operand(operand)
    assert isinstance(r, ExtendedIndirect)

def test_list_causes_indirection_for_label():
    address = Label('loop')
    operand = [{address}]
    r = parse_operand(operand)
    assert isinstance(r, ExtendedIndirect)

# TODO: Indexed addressing
