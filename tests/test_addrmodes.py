from pytest import raises

from asm68.addrmodes import PageDirect, ExtendedDirect, ExtendedIndirect


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