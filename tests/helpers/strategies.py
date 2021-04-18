from hypothesis import assume
from hypothesis.strategies import from_regex, text, composite

from string import ascii_uppercase

from asm68.util import is_valid_variable_name


from helpers.alphabets import ASCII_UPPERCASE_AND_DIGITS

@composite
def label_names(draw):
    label_name = draw(from_regex(r'\A[A-Za-z][A-Za-z0-9_]*\Z'))
    assume(is_valid_variable_name(label_name))
    return label_name


@composite
def mnemonics(draw, min_size=1):
    if min_size < 0:
        raise ValueError("mnemonics(min_size={}) is negative".format(min_size))
    a_size = min(min_size, 1)
    b_size = min_size - a_size
    a = draw(text(min_size=a_size, max_size=1, alphabet=ascii_uppercase))
    b = draw(text(min_size=b_size, alphabet=ASCII_UPPERCASE_AND_DIGITS))
    return a + b
