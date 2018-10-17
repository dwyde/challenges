#!/usr/bin/env python3
"""
FIXME: needs code cleanup...
"""

import collections
import json
import os
import shutil

import yaml


BASE_PORT = 9000

SCOREBOARD_PORT = 9000

THIS_DIR = os.path.dirname(__file__)

BASE_DIR = os.path.join(THIS_DIR, '..')

FIXTURES_FILE = os.path.join(BASE_DIR, 'scoreboard', 'challenges',
                             'fixtures', 'challenges.yaml')

COMPOSE_FILE = os.path.join(BASE_DIR, 'docker-compose.yml')

DJANGO_CHALLENGE_MODEL = 'challenges.challenge'


def read_services(filename):
    with open(filename) as service_file:
        return yaml.safe_load(service_file)


def get_challenge_json(name):
    path = os.path.join(BASE_DIR, 'challenges', name, 'challenge.json')
    with open(path) as fp:
        return json.load(fp)


def get_public_port(index):
    return str(BASE_PORT + index)


def generate_fixture(name, index):
    challenge_json = get_challenge_json(name)
    fixture = {
        'model': DJANGO_CHALLENGE_MODEL,
        'pk': index,
        'fields': {
            'name': name,
            'display_name': challenge_json['displayname'],
            'port': get_public_port(index),
            'description': challenge_json['desc'],
            'points': challenge_json['basescore'],
            'flag': challenge_json['flag'],
            'category': challenge_json['category'],
        }
    }
    return fixture, challenge_json['port']


def collect_static(name):
    source = os.path.join(BASE_DIR, 'challenges', name, 'static')
    dest = os.path.join(BASE_DIR, 'scoreboard', 'challenges', 'static', name)
    try:
        shutil.rmtree(dest)
    except FileNotFoundError:
        pass

    try:
        shutil.copytree(source, dest)
    except FileNotFoundError:
        pass


def _init_yaml_ordereddict():
    def ordered_dict_presenter(dumper, data):
        return dumper.represent_dict(data.items())
    yaml.add_representer(collections.OrderedDict, ordered_dict_presenter)


def main():
    _init_yaml_ordereddict()

    service_file = os.path.join(THIS_DIR, 'services.yml')
    services = read_services(service_file)

    fixtures = []
    compose = collections.OrderedDict()
    for i, name in enumerate(services, -1):
        if name == 'scoreboard':
            compose[name] = {
                'build': name,
                'ports': [str(BASE_PORT) + ':' + str(SCOREBOARD_PORT)],
                'depends_on': ['database']
            }
        elif name == 'database':
            compose[name] = {
                'image': 'postgres',
                'volumes': ['./db_data:/var/lib/postgresql/data']
            }
        else:
            entry, port = generate_fixture(name, i)
            fixtures.append(entry)
            collect_static(name)
            if port:
                compose[name] = {
                    'build': os.path.join('challenges', name),
                    'ports': [str(BASE_PORT + i) + ':' + str(port)]
                }

    with open(FIXTURES_FILE, 'w') as outfile:
        yaml.dump(fixtures, outfile)

    with open(COMPOSE_FILE, 'w') as compose_file:
        compose_file.write('version: "2.1"\n')
        yaml.dump({'services': compose}, compose_file)


if __name__ == '__main__':
    main()
