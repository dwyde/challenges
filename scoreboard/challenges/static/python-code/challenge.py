"""
A Python puzzle: get the `code` type.
"""
import re
import types


# Validate input for safety: match this regular expression.
PATTERN = re.compile(r'^[a-z0-9_\.:[\]]{,32}$')

# A placeholder for the flag.
FLAG = object()


def pre_eval(value):
    """ Check the value before later calling `eval()` on it.
    """
    if PATTERN.match(value) is None:
        raise ValueError('Input must match the pattern: %s' % PATTERN.pattern)


def check_object(value):
    """ `eval()` a value, and see if it's the `code` type.
    """
    obj = eval(value, {})
    if obj is not types.CodeType:
        raise ValueError('That is not the right object!')


def main(user_input):
    """
    Enter something that evaluates to Python's `code` type.
    """
    pre_eval(user_input)
    check_object(user_input)
    return FLAG

