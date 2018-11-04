import sys

import flag
del flag


class A(object):
    def __init__(self):
        pass


def main(user_input):
    obj = A()
    result = user_input.format(obj)
    return result


if __name__ == '__main__':
    import sys 
    user_input = sys.stdin.readline().strip()
    result = main(user_input)
    print(result)

