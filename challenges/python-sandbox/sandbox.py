""" A Python 3 challenge: get a flag from a sandbox.
"""
import sys


# Limit the size of user input.
MAX_INPUT_CHARACTERS = 200


def get_builtins():
    """ Get built-in objects, in different contexts.
    """
    try:
        builtins = __builtins__.__dict__
    except AttributeError:
        builtins = __builtins__

    return builtins.copy()


def build_namespace():
    """ Restrict built-in functions, for `exec()`.
    """
    builtins = get_builtins()
    banned_functions = [
        'compile', 'eval', 'exec', 'exit', 'help',
        '__import__', 'input', '__loader__', 'print'
    ]
    for func in banned_functions:
        del builtins[func]
    return {'__builtins__': builtins}


def run_code(user_input):
    """ Run code in a sandbox.
    """
    namespace = build_namespace()
    try:
        exec(user_input, namespace)
    except Exception as e:
        return str(e)
    else:
        with open('flag') as flag:
            # TODO: handle result
            return 'Your code ran!'


def sandbox(user_input):
    """ Check the user's code, then run it.
    """
    if len(user_input) > MAX_INPUT_CHARACTERS:
        message = 'Input cannot be longer than {} characters.'
        return message.format(MAX_INPUT_CHARACTERS)

    # Only allow certain characters.
    whitelist = set('abcdefghijklmnopqrstuvwxyz~!@#$%^&*-%+=:/0123456789\n ')
    difference = set(user_input) - whitelist
    if difference:
        message = ''.join(sorted(difference))
        return 'Forbidden character(s): {}'.format(message)
    else:
        return run_code(user_input)


def main():
    solution = sys.stdin.read()
    result = sandbox(solution)
    print(result)


if __name__ == '__main__':
    main()
