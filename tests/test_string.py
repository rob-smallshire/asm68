from asm68.stringutil import upper_first, uppercase_ending


def test_upper_first_empty():
    assert upper_first("") == ""


def test_upper_first_single():
    assert upper_first("a") == "A"


def test_upper_first_multiple():
    assert upper_first("aardvark") == "Aardvark"


def test_upper_first_idempotent():
    assert upper_first("Aardvark") == "Aardvark"


def test_upper_first_preserves_case_after_first():
    assert upper_first("AaDvArK") == "AaDvArK"


def test_last_if_uppercase_ending_empty():
    assert uppercase_ending("") == ""


def test_single_last_if_uppercase_ending_positive():
    assert uppercase_ending("J") == "J"


def test_single_last_if_uppercase_ending_negative():
    assert uppercase_ending("j") == ""


def test_multiple_last_if_uppercase_ending_positive():
    assert uppercase_ending("IncF") == "F"


def test_multiple_last_if_uppercase_ending_negative():
    assert uppercase_ending("Incf") == ""


def test_multiple_last_if_uppercase_ending_positive_multiple():
    assert uppercase_ending("AndCC") == "CC"
