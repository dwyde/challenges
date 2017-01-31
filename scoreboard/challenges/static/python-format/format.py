import sys

import flag
del flag


class A(object):
    def __init__(self):
        pass

line = sys.stdin.readline()
result = line.format(A())
print(result)

