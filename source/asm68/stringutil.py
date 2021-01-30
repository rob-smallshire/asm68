import re

def upper_first(s):
    """The input string with the first character in uppercase.
    """
    return s[0:1].upper() + s[1:]


UPPERCASE_ENDING_PATTERN = r'[A-Za-z0-9]*?([A-Z]*)$'
UPPERCASE_ENDING_REGEX = re.compile(UPPERCASE_ENDING_PATTERN)


def uppercase_ending(s):
    """The contiguous uppercase end of the string, or an empty string.
    """
    return UPPERCASE_ENDING_REGEX.match(s).group(1)
