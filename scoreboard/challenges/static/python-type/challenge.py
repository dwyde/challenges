"""
A Python puzzle: use "type" after __builtins__ are removed.
"""
import sys


MAX_LENGTH = 100


def check_safety(text):
    if len(text) > MAX_LENGTH:
        raise ValueError('Your input was too long.')
    if '(' in text:
        raise ValueError('No parentheses allowed!')


def evals_to_type(text):
    """ Eval a value, and return whether it's the `type` object.
    """
    try:
        result = eval(text, {'__builtins__': {}})
    except Exception:
        result = None
    return result is type


def main():
    """ Ask for input until EOF or KeyboardInterrupt.
    """
    user_input = sys.stdin.readline()
    check_safety(user_input)
    if evals_to_type(user_input):
        with open('flag') as fp:
            print(fp.read())
    else:
        print('Try again!')

if __name__ == '__main__':
    main()
