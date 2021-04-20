from pytest import raises

from asm68.contiguous_bytes import ContiguousBytes


def test_empty_continuous_bytes():
    ContiguousBytes()


def test_empty_continuous_bytes_has_zero_length():
    cb = ContiguousBytes()
    assert len(cb) == 0


def test_single_block_empty_block_has_zero_length():
    blocks = {0: b''}
    cb = ContiguousBytes(blocks)
    assert len(cb) == 0


def test_single_non_empty_block_at_zero_address_has_expected_length():
    blocks = {0: b'Hello'}
    cb = ContiguousBytes(blocks)
    assert len(cb) == 5


def test_single_non_empty_block_at_nonzero_address_has_expected_length():
    blocks = {35: b'Hello'}
    cb = ContiguousBytes(blocks)
    assert len(cb) == 5


def test_implicit_start_address_respected():
    blocks = {23: b'Hello'}
    cb = ContiguousBytes(blocks)
    assert cb.start == 23


def test_explicit_start_address_before_first_block_respected():
    blocks = {23: b'Hello'}
    cb = ContiguousBytes(blocks, start=20)
    assert cb.start == 20


def test_explicit_start_address_at_first_block_respected():
    blocks = {23: b'Hello'}
    cb = ContiguousBytes(blocks, start=23)
    assert cb.start == 23


def test_explicit_start_address_after_first_block_raises_value_error():
    blocks = {0: b'Hello'}
    with raises(ValueError):
        _ = ContiguousBytes(blocks, start=1)


def test_implicit_stop_address_respected():
    blocks = {
        23: b'Hello',
        47: b'World',
    }
    cb = ContiguousBytes(blocks)
    assert cb.stop == 52


def test_explicit_stop_after_last_block_respected():
    blocks = {
        23: b'Hello',
        47: b'World',
    }
    cb = ContiguousBytes(blocks, stop=57)
    assert cb.stop == 57


def test_explicit_stop_at_last_block_respected():
    blocks = {
        23: b'Hello',
        47: b'World',
    }
    cb = ContiguousBytes(blocks, stop=52)
    assert cb.stop == 52


def test_explicit_stop_before_last_block_raises_value_error():
    blocks = {
        23: b'Hello',
        47: b'World',
    }
    with raises(ValueError):
        _ = ContiguousBytes(blocks, stop=51)


def test_explicit_stop_before_explicit_start_raises_value_error():
    with raises(ValueError):
        _ = ContiguousBytes(start=51, stop=50)


def test_overlapping_blocks_raises_value_error():
    blocks = {
        23: b'Hello',
        27: b'World',
    }
    with raises(ValueError):
        _ = ContiguousBytes(blocks)


def test_negative_start_raises_value_error():
    with raises(ValueError):
        _ = ContiguousBytes(start=-1)


def test_negative_stop_raises_value_error():
    with raises(ValueError):
        _ = ContiguousBytes(stop=-1)


def test_empty_with_nonzero_start_address_has_zero_length():
    cb = ContiguousBytes(start=32768)
    assert len(cb) == 0


def test_default_stop_address_is_start_address():
    cb = ContiguousBytes(start=1234)
    assert cb.stop == 1234


def test_negative_block_address_raises_value_error():
    blocks = {
        -1: b'Hello',
    }
    with raises(ValueError):
        _ = ContiguousBytes(blocks)


def test_lookup_before_start_raises_key_error():
    blocks = {
        5: b'Hello',
    }
    cb = ContiguousBytes(blocks)
    with raises(KeyError):
        _ = cb[4]


def test_lookup_after_end_raises_key_error():
    blocks = {
        5: b'Hello',
    }
    cb = ContiguousBytes(blocks)
    with raises(KeyError):
        _ = cb[10]


def test_iteration_over_contiguous_blocks():
    blocks = {
        5: b'Hello',
        10: b", World!"
    }
    cb = ContiguousBytes(blocks)
    whole = bytes(cb.values())
    assert whole == b'Hello, World!'



def test_iteration_before_first_block():
    blocks = {
        5: b'Hello',
        12: b", World!"
    }
    cb = ContiguousBytes(blocks, start=0)
    whole = cb.to_bytes()
    assert whole == b'\x00\x00\x00\x00\x00Hello\x00\x00, World!'


def test_iteration_after_last_block():
    blocks = {
        5: b'Hello',
        12: b", World!"
    }
    cb = ContiguousBytes(blocks, stop=23)
    whole = cb.to_bytes()
    assert whole == b'Hello\x00\x00, World!\x00\x00\x00'


def test_iteration_over_separated_blocks():
    blocks = {
        5: b'Hello',
        12: b", World!"
    }
    cb = ContiguousBytes(blocks)
    whole = cb.to_bytes()
    assert whole == b'Hello\x00\x00, World!'


def test_iteration_over_separated_blocks_respects_default():
    blocks = {
        5: b'Hello',
        12: b", World!"
    }
    cb = ContiguousBytes(blocks, default=0xff)
    whole = cb.to_bytes()
    assert whole == b'Hello\xff\xff, World!'


def test_keys_start():
    blocks = {
        5: b'Hello',
        12: b", World!"
    }
    cb = ContiguousBytes(blocks)
    assert cb.keys().start == 5


def test_keys_getitem():
    blocks = {
        5: b'Hello',
        12: b", World!"
    }
    cb = ContiguousBytes(blocks)
    assert cb.keys()[0] == 5


def test_keys_len():
    blocks = {
        5: b'Hello',
        12: b", World!"
    }
    cb = ContiguousBytes(blocks)
    assert len(cb.keys()) == 15


def test_keys_repr():
    blocks = {
        5: b'Hello',
        12: b", World!"
    }
    cb = ContiguousBytes(blocks)
    assert repr(cb.keys()) == "RangeSet(start=5, stop=20)"

