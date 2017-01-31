import ast
import os.path
import string


# Maximum input length
MAX_LENGTH = 8

# Allowed characters
CHARACTER_SET = set(string.ascii_lowercase + string.punctuation)


def check_length(value):
    if len(value) > MAX_LENGTH:
        message = 'Input cannot be longer than {}.'
        raise ValueError(message.format(MAX_LENGTH))


def check_allowed_characters(value):
    if set(value) - CHARACTER_SET:
        message = 'Only these characters are allowed: {}'
        allowed_chars = ''.join(sorted(CHARACTER_SET))
        raise ValueError(message.format(allowed_chars))


def check_eval_result(value):
    to_eval = '1-1{}chance'.format(value)
    try:
        result = ast.literal_eval(to_eval)
    except Exception:
        raise ValueError('ast.literal_eval() call failed.')
    else:
        if result == 0:
            raise ValueError('The result must not be 0.')


def read_flag():
    """ Read in this challenge's flag.
    """
    path = os.path.join(os.path.dirname(__file__), 'flag')
    with open(path) as fp:
        return fp.read().strip()


def main(user_input):
    check_length(user_input)
    check_allowed_characters(user_input)
    check_eval_result(user_input)
    return read_flag()


if __name__ == '__main__':
   import sys
   user_input = sys.stdin.readline().strip()
   result = main(user_input)
   print(result)
