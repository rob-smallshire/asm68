from pytest import raises
from hypothesis import given, assume
from hypothesis.strategies import integers, sets, sampled_from, one_of, lists

from asm68.addrmodes import (PageDirect, ExtendedDirect, ExtendedIndirect, Inherent, Immediate, Registers, Indexed,
                             Relative, Integers)
from asm68.registers import REGISTERS, INDEX_REGISTERS, ACCUMULATORS
from tests.predicates import check_balanced


def test_inherent_equality():
    assert Inherent() == Inherent()

def test_inherent_inequality():
    assert Inherent() != object()

def test_inherent_repr():
    r = repr(Inherent())
    assert r.startswith('Inherent')
    assert check_balanced(r)

def test_inherent_hash():
    assert hash(Inherent()) == hash(Inherent())

@given(a=integers())
def test_immediate_value(a):
    assert Immediate(a).value == a

@given(a=integers())
def test_immediate_repr(a):
    r = repr(Immediate(a))
    assert r.startswith('Immediate')
    assert str(a) in r
    assert check_balanced(r)

@given(a=integers())
def test_immediate_equality(a):
    assert Immediate(a) == Immediate(a)

@given(a=integers(), b=integers())
def test_immediate_inequality(a, b):
    assume(a != b)
    assert Immediate(a) != Immediate(b)

@given(a=integers())
def test_immediate_inequality_different_types(a):
    assert Immediate(a) != object()

@given(a=integers())
def test_immediate_hash(a):
    assert hash(Immediate(a)) == hash(Immediate(a))

def test_empty_registers_raises_value_error():
    t = tuple()
    with raises(ValueError):
        Registers(t)

@given(s=sets(elements=sampled_from(sorted(REGISTERS)), min_size=1))
def test_registers_value(s):
    t = tuple(s)
    assert Registers(t).registers == t

@given(s=sets(elements=sampled_from(sorted(REGISTERS)), min_size=1))
def test_registers_equality(s):
    u = tuple(s)
    v = tuple(s)
    assert Registers(u) == Registers(v)

@given(s=sets(elements=sampled_from(sorted(REGISTERS)), min_size=1),
       t=sets(elements=sampled_from(sorted(REGISTERS)), min_size=1))
def test_registers_inequality(s, t):
    assume(s != t)
    u = tuple(s)
    v = tuple(t)
    assert Registers(u) != Registers(v)

@given(s=sets(elements=sampled_from(sorted(REGISTERS)), min_size=1))
def test_registers_inequality_different_types(s):
    u = tuple(s)
    assert Registers(u) != object()

@given(s=sets(elements=sampled_from(sorted(REGISTERS)), min_size=1))
def test_registers_hash_equal(s):
    u = tuple(s)
    v = tuple(s)
    assert hash(Registers(u)) == hash(Registers(v))

@given(s=sets(elements=sampled_from(sorted(REGISTERS)), min_size=1))
def test_registers_repr(s):
    r = repr(Registers(s))
    assert r.startswith('Registers')
    assert all(register.name in r for register in s)
    assert check_balanced(r)

def test_page_direct_address_must_be_one_byte():
    address = 0x34
    r = PageDirect(address)
    assert r.address == address

def test_page_direct_negative_address_raises_value_error():
    address = -1
    with raises(ValueError):
        PageDirect(address)

def test_page_direct_two_byte_address_raises_value_error():
    address = 0x0100
    with raises(ValueError):
        PageDirect(address)

@given(address=integers(min_value=0x00, max_value=0xFF))
def test_page_direct_repr(address):
    r = repr(PageDirect(address))
    assert r.startswith('PageDirect')
    assert hex(address)[2:].upper() in r
    assert check_balanced(r)

@given(address=integers(min_value=0x00, max_value=0xFF))
def test_page_direct_equality(address):
    assert PageDirect(address) == PageDirect(address)

@given(a=integers(min_value=0x00, max_value=0xFF),
       b=integers(min_value=0x00, max_value=0xFF))
def test_page_direct_inequality(a, b):
    assume(a != b)
    assert PageDirect(a) != PageDirect(b)

@given(address=integers(min_value=0x00, max_value=0xFF))
def test_page_direct_inequality_different_types(address):
    assert PageDirect(address) != object()

@given(address=integers(min_value=0x00, max_value=0xFF))
def test_page_direct_equal_hash(address):
    assert hash(PageDirect(address)) == hash(PageDirect(address))

def test_extended_direct_incorrect_type_raises_type_error():
    with raises(TypeError):
        ExtendedDirect(object())

@given(address=integers(min_value=0x0000, max_value=0xFFFF))
def test_extended_direct_address_must_be_two_byte(address):
    r = ExtendedDirect(address)
    assert r.address == address

@given(address=integers(max_value=-1))
def test_negative_extended_direct_address_raises_value_error(address):
    with raises(ValueError):
        ExtendedDirect(address)

@given(address=integers(min_value=0x10000))
def test_extended_direct_three_byte_address_raises_value_error(address):
    address = 0x010000
    with raises(ValueError):
        ExtendedDirect(address)

@given(address=integers(min_value=0x0000, max_value=0xFFFF))
def test_extended_direct_repr(address):
    r = repr(ExtendedDirect(address))
    assert r.startswith('ExtendedDirect')
    assert hex(address)[2:].upper() in r
    assert check_balanced(r)

@given(a=integers(min_value=0x0000, max_value=0xFFFF),
       b=integers(min_value=0x0000, max_value=0xFFFF))
def test_extended_direct_inequality(a, b):
    assume(a != b)
    assert ExtendedDirect(a) != ExtendedDirect(b)

@given(address=integers(min_value=0x0000, max_value=0xFFFF))
def test_extended_direct_inequality_different_types(address):
    assert ExtendedDirect(address) != object()

@given(address=integers(min_value=0x0000, max_value=0xFFFF))
def test_extended_direct_equal_hash(address):
    assert hash(ExtendedDirect(address)) == hash(ExtendedDirect(address))

def test_extended_indirect_incorrect_type_raises_type_error():
    with raises(TypeError):
        ExtendedIndirect(object())

@given(address=integers(min_value=0x0000, max_value=0xFFFF))
def test_extended_indirect_address_must_be_two_byte(address):
    r = ExtendedIndirect(address)
    assert r.address == address

@given(address=integers(max_value=-1))
def test_negative_extended_indirect_address_raises_value_error(address):
    with raises(ValueError):
        ExtendedIndirect(address)

@given(address=integers(min_value=0x10000))
def test_extended_indirect_three_byte_address_raises_value_error(address):
    address = 0x010000
    with raises(ValueError):
        ExtendedIndirect(address)

@given(address=integers(min_value=0x0000, max_value=0xFFFF))
def test_extended_indirect_repr(address):
    r = repr(ExtendedIndirect(address))
    assert r.startswith('ExtendedIndirect')
    assert hex(address)[2:].upper() in r
    assert check_balanced(r)

@given(a=integers(min_value=0x0000, max_value=0xFFFF),
       b=integers(min_value=0x0000, max_value=0xFFFF))
def test_extended_indirect_inequality(a, b):
    assume(a != b)
    assert ExtendedIndirect(a) != ExtendedIndirect(b)

@given(address=integers(min_value=0x0000, max_value=0xFFFF))
def test_extended_indirect_inequality_different_types(address):
    assert ExtendedIndirect(address) != object()

@given(address=integers(min_value=0x0000, max_value=0xFFFF))
def test_extended_indirect_equal_hash(address):
    assert hash(ExtendedIndirect(address)) == hash(ExtendedIndirect(address))

@given(base=sampled_from(sorted(INDEX_REGISTERS)),
       offset=one_of(sampled_from(sorted(ACCUMULATORS)),
                     integers(min_value=0x0000, max_value=0xFFFF)))
def test_indexed_values(base, offset):
    idx = Indexed(base, offset)
    assert idx.base == base
    assert idx.offset == offset

@given(base=sampled_from(sorted(INDEX_REGISTERS)),
       offset=one_of(sampled_from(sorted(ACCUMULATORS)),
                     integers(min_value=0x0000, max_value=0xFFFF)))
def test_indexed_repr(base, offset):
    r = repr(Indexed(base, offset))
    assert r.startswith('Indexed')
    assert base.name in r
    assert check_balanced(r)

@given(base=sampled_from(sorted(INDEX_REGISTERS)),
       offset=one_of(sampled_from(sorted(ACCUMULATORS)),
                     integers(min_value=0x0000, max_value=0xFFFF)))
def test_indexed_equality(base, offset):
    assert Indexed(base, offset) == Indexed(base, offset)

@given(base=sampled_from(sorted(INDEX_REGISTERS)),
       offset=one_of(sampled_from(sorted(ACCUMULATORS)),
                     integers(min_value=0x0000, max_value=0xFFFF)))
def test_indexed_inequality_different_types(base, offset):
    assert Indexed(base, offset) != object()


@given(base_a=sampled_from(sorted(INDEX_REGISTERS)),
       offset_a=one_of(sampled_from(sorted(ACCUMULATORS)),
                     integers(min_value=0x0000, max_value=0xFFFF)),
       base_b=sampled_from(sorted(INDEX_REGISTERS)),
       offset_b=one_of(sampled_from(sorted(ACCUMULATORS)),
                     integers(min_value=0x0000, max_value=0xFFFF)))
def test_indexed_inequality(base_a, offset_a, base_b, offset_b):
    assume((base_a, offset_a) != (base_b, offset_b))
    assert Indexed(base_a, offset_a) != Indexed(base_b, offset_b)

@given(base=sampled_from(sorted(INDEX_REGISTERS)),
       offset=one_of(sampled_from(sorted(ACCUMULATORS)),
                     integers(min_value=0x0000, max_value=0xFFFF)))
def test_indexed_hash_equality(base, offset):
    assert hash(Indexed(base, offset)) == hash(Indexed(base, offset))

@given(offset=integers(min_value=0x00, max_value=0xFF))
def test_relative_value(offset):
    assert Relative(offset).offset == offset

@given(offset=integers(max_value=-1))
def test_relative_negative_offsets_raise_value_error(offset):
    with raises(ValueError):
        Relative(offset)

@given(offset=integers(min_value=0x10000))
def test_relative_two_byte_offsets_raise_value_error(offset):
    with raises(ValueError):
        Relative(offset)

@given(offset=integers(min_value=0x00, max_value=0xFF))
def test_relative_repr(offset):
    r = repr(Relative(offset))
    assert r.startswith('Relative')
    assert str(offset) in r
    assert check_balanced(r)

@given(offset=integers(min_value=0x00, max_value=0xFF))
def test_relative_equality(offset):
    assert Relative(offset) == Relative(offset)

@given(a=integers(min_value=0x00, max_value=0xFF),
       b=integers(min_value=0x00, max_value=0xFF))
def test_relative_inequality(a, b):
    assume(a != b)
    assert Relative(a) != Relative(b)

@given(offset=integers(min_value=0x00, max_value=0xFF))
def test_relative_inequality_different_types(offset):
    assert Relative(offset) != object()

@given(offset=integers(min_value=0x00, max_value=0xFF))
def test_relative_equal_hash(offset):
    assert hash(Relative(offset)) == hash(Relative(offset))

@given(items=lists(elements=integers(min_value=0x0000, max_value=0xFFFF), min_size=1))
def test_integers_values(items):
    assert list(Integers(items)) == items

def test_integers_empty_raises_value_error():
    with raises(ValueError):
        Integers([])

def test_items_are_integers():
    with raises(TypeError):
        Integers(["hello"])

@given(items=lists(elements=integers(min_value=0x0000, max_value=0xFFFF), min_size=1))
def test_integers_repr(items):
    r = repr(Integers(items))
    assert r.startswith('Integers')
    assert check_balanced(r)

@given(items=lists(elements=integers(min_value=0x0000, max_value=0xFFFF), min_size=1))
def test_integers_equality(items):
    assert Integers(items) == Integers(items)

@given(items_a=lists(elements=integers(min_value=0x0000, max_value=0xFFFF), min_size=1),
       items_b=lists(elements=integers(min_value=0x0000, max_value=0xFFFF), min_size=1))
def test_integers_inequality(items_a, items_b):
    assume(items_a != items_b)
    assert Integers(items_a) != Integers(items_b)

@given(items=lists(elements=integers(min_value=0x0000, max_value=0xFFFF), min_size=1))
def test_integers_inequality_different_types(items):
    assert Integers(items) != object()

@given(items=lists(elements=integers(min_value=0x0000, max_value=0xFFFF), min_size=1))
def test_integers_equal_hash(items):
    assert hash(Integers(items)) == hash(Integers(items))