import reprlib
from keyword import iskeyword


def single(iterable):
    i = iter(iterable)
    try:
        value = next(i)
    except StopIteration:
        raise ValueError("Expected one item. Too few items in {}".format(reprlib.repr(iterable)))
    try:
        next(i)
        raise ValueError("Expected one item. Too many items in {}".format(reprlib.repr(iterable)))
    except StopIteration:
        return value


def is_valid_variable_name(name):
    return name.isidentifier() and not iskeyword(name)


def take_after(predicate, iterable):
    found = False
    for item in iterable:
        found = found or predicate(item)
        if found:
            yield item
            
            
def typename(obj):
    return type(obj).__name__