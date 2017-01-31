#!/usr/bin/env python3

import json
import os.path
import shutil

import yaml


BASE_DIR = os.path.dirname(__file__)

FIXTURES_FILE = os.path.join(BASE_DIR, 'scoreboard', 'challenges',
                             'fixtures', 'challenges.yaml')

DJANGO_CHALLENGE_MODEL = 'challenges.challenge'


def read_docker_compose(filename):
    with open(filename) as compose_file:
        return yaml.safe_load(compose_file)


def get_challenge_json(name):
    path = os.path.join(BASE_DIR, 'challenges', name, 'challenge.json')
    with open(path) as fp:
        return json.load(fp)


def get_public_port(service):
    mapping = service['ports'][0]
    public, _ = mapping.split(':', 1)
    return public


def generate_fixture(name, service, index):
    challenge_json = get_challenge_json(name)
    return {
        'model': DJANGO_CHALLENGE_MODEL,
        'pk': index,
        'fields': {
            'name': name,
            'display_name': challenge_json['displayname'],
            'port': get_public_port(service),
            'description': challenge_json['desc'],
            'points': challenge_json['basescore'],
            'flag': challenge_json['flag'],
        }
    }


def collect_static(name):
    source = os.path.join(BASE_DIR, 'challenges', name, 'static')
    dest = os.path.join(BASE_DIR, 'scoreboard', 'challenges', 'static', name)
    try:
        shutil.rmtree(dest)
        shutil.copytree(source, dest)
    except (FileExistsError, FileNotFoundError):
        pass


def main():
    compose = read_docker_compose('docker-compose.yml')

    fixtures = []
    for i, (name, service) in enumerate(compose['services'].items()):
        if name != 'scoreboard':
            entry = generate_fixture(name, service, i)
            fixtures.append(entry)
            collect_static(name)

    with open(FIXTURES_FILE, 'w') as outfile:
        yaml.dump(fixtures, outfile)


if __name__ == '__main__':
    main()
