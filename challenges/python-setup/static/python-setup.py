import os.path


# Maximum input length: code golf :-)
MAX_LENGTH = 12

# Allowed input characters
CHARACTER_SET = set('abcd3fghijklmnopqrstuvwxyz{}[]')


def check_length(value):
    if len(value) > MAX_LENGTH:
        message = 'Input length cannot be longer than {}.'
        raise ValueError(message.format(MAX_LENGTH))


def check_for_forbidden_characters(value):
    input_difference = set(value) - CHARACTER_SET
    if input_difference:
        message = 'You used forbidden characters: {}.'
        raise ValueError(message.format(input_difference))


def check_equals_empty_set(value):
    try:
        result = eval(value, {})
    except Exception:
        raise ValueError('eval() failed')

    if result != set():
        raise ValueError('You failed to set() me up!')


def read_flag():
    """ Read in this challenge's flag.
    """
    path = os.path.join(os.path.dirname(__file__), 'flag')
    with open(path) as fp:
        return fp.read().strip()


def main(user_input):
    check_length(user_input)
    check_for_forbidden_characters(user_input)
    check_equals_empty_set(user_input)
    return read_flag()


if __name__ == '__main__':
    import sys 
    user_input = sys.stdin.readline().strip()
    result = main(user_input)
    print(result)

