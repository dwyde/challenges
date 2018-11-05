import os.path
import re

import yaml


def read_flag():
    """ Read this challenge's flag.
    """
    path = os.path.join(os.path.dirname(__file__), 'flag')
    with open(path) as fp:
        return fp.read().strip()


def main(user_input):
    """ Use YAML to load a name, with constraints.
    """
    if re.search(r'[^A-Za-z\.]', user_input):
        raise ValueError('Invalid input')

    text = '!!python/name:{}er'.format(user_input)
    obj = yaml.load(text)
    if '__hash__' in vars(obj):
        return read_flag()

