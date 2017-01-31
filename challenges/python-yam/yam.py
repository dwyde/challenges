import re
import sys

import yaml


user_input = sys.stdin.readline().strip()
if re.search(r'[^A-Za-z\.]', user_input):
    raise ValueError('Invalid input')

text = '!!python/name:{}er'.format(user_input)
obj = yaml.load(text)
if '__hash__' in vars(obj):
    with open('flag') as fp:
        print(fp.read())
