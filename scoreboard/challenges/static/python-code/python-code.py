"""
A Python puzzle: get the `code` type.
"""
import os.path
import re
import types


# Validate input for safety: match this regular expression.
PATTERN = re.compile(r'^[a-z0-9_\.:[\]]{,32}$')


def pre_eval(value):
    """ Check the value before later calling `eval()` on it.
    """
    if PATTERN.match(value) is None:
        raise ValueError('Input must match the pattern: %s' % PATTERN.pattern)


def check_object(value):
    """ `eval()` a value, and see if it's the `code` type.
    """
    obj = eval(value, {'__builtins__': {}})
    if obj is not types.CodeType:
        raise ValueError('That is not the right object!')


def read_flag():
    """ Read this challenge's flag.
    """
    path = os.path.join(os.path.dirname(__file__), 'flag')
    with open(path) as fp:
        return fp.read().strip()


def main(user_input):
    """
    Enter something that evaluates to Python's `code` type.
    """
    pre_eval(user_input)
    check_object(user_input)
    return read_flag()


if __name__ == '__main__':
    import sys
    user_input = sys.stdin.readline().strip()
    result = main(user_input)
    print(result)

