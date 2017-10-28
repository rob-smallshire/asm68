from pytest import raises
from hypothesis import given, assume
from hypothesis.strategies import integers, sets, sampled_from

from asm68.addrmodes import (PageDirect, ExtendedDirect, ExtendedIndirect, Inherent, Immediate, Registers)
from asm68.registers import A, B, D, E, F, W, Q, X, Y, U, S, DP, CC, MD


def test_inherent_equality():
    assert Inherent() == Inherent()

def test_inherent_inequality():
    assert Inherent() != object()

def test_inherent_repr():
    r = repr(Inherent())
    assert r == 'Inherent()'

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

@given(s=sets(elements=sampled_from((A, B, D, E, F, W, Q, X, Y, U, S, DP, CC, MD)), min_size=1))
def test_registers_value(s):
    t = tuple(s)
    assert Registers(t).registers == t

@given(s=sets(elements=sampled_from((A, B, D, E, F, W, Q, X, Y, U, S, DP, CC, MD)), min_size=1))
def test_registers_equality(s):
    u = tuple(s)
    v = tuple(s)
    assert Registers(u) == Registers(v)

@given(s=sets(elements=sampled_from((A, B, D, E, F, W, Q, X, Y, U, S, DP, CC, MD)), min_size=1),
       t=sets(elements=sampled_from((A, B, D, E, F, W, Q, X, Y, U, S, DP, CC, MD)), min_size=1))
def test_registers_inequality(s, t):
    assume(s != t)
    u = tuple(s)
    v = tuple(t)
    assert Registers(u) != Registers(v)

@given(s=sets(elements=sampled_from((A, B, D, E, F, W, Q, X, Y, U, S, DP, CC, MD)), min_size=1))
def test_registers_inequality_different_types(s):
    u = tuple(s)
    assert Registers(u) != object()

@given(s=sets(elements=sampled_from((A, B, D, E, F, W, Q, X, Y, U, S, DP, CC, MD)), min_size=1))
def test_registers_hash_equal(s):
    u = tuple(s)
    v = tuple(s)
    assert hash(Registers(u)) == hash(Registers(v))

@given(s=sets(elements=sampled_from((A, B, D, E, F, W, Q, X, Y, U, S, DP, CC, MD)), min_size=1))
def test_registers_repr(s):
    r = repr(Registers(s))
    assert r.startswith('Registers')
    assert all(register.name in r for register in s)

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

def test_extended_direct_address_must_be_two_byte():
    address = 0x3F2A
    r = ExtendedDirect(address)
    assert r.address == address

def test_negative_extended_direct_address_raises_value_error():
    address = -1
    with raises(ValueError):
        ExtendedDirect(address)

def test_extended_direct_one_byte_address_raises_value_error():
    address = 0xFF
    with raises(ValueError):
        ExtendedDirect(address)

def test_extended_direct_three_byte__address_raises_value_error():
    address = 0x010000
    with raises(ValueError):
        ExtendedDirect(address)

def test_negative_extended_indirect_address_raises_value_error():
    address = -1
    with raises(ValueError):
        ExtendedIndirect(address)

def test_extended_indirect_three_byte__address_raises_value_error():
    address = 0x010000
    with raises(ValueError):
        ExtendedIndirect(address)

