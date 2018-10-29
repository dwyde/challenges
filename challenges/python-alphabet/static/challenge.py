import os.path


# Mandatory characters
CHARACTER_SET = sorted('[[abcdefghijklmnopqrstuvwxyz]]')


def check_valid_characters(value):
    """ Check that the user supplied proper characters.
    """
    if sorted(value) != CHARACTER_SET:
        message = 'Input must use exactly these {} characters: {}'
        formatted = message.format(len(CHARACTER_SET), ''.join(CHARACTER_SET))
        raise ValueError(formatted)


def check_eval(value):
    """ Evaluate a Python expression.
    """
    try:
        eval(value, {})
    except Exception:
        raise ValueError('The call to `eval()` failed.')


def read_flag():
    """ Read in this challenge's flag.
    """
    path = os.path.join(os.path.dirname(__file__), 'flag')
    with open(path) as fp:
        return fp.read().strip()


def main(user_input):
    """ Run the challenge.
    """
    check_valid_characters(user_input)
    check_eval(user_input)
    return read_flag()


if __name__ == '__main__':
    import sys 
    user_input = sys.stdin.read().strip()
    result = main(user_input)
    print(result)

