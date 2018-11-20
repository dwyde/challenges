#!/usr/bin/env python3
"""
FIXME: needs code cleanup...
"""
import argparse
import collections
import json
import os
import shutil

import yaml


LOCALHOST = '127.0.0.1'

BASE_PORT = 9000

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
    path = os.path.join(BASE_DIR, 'challenges', name, 'metadata.json')
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


def challenge_config_and_static_files(use_tls, use_vagrant):
    _init_yaml_ordereddict()

    service_file = os.path.join(THIS_DIR, 'services.yml')
    services = read_services(service_file)

    fixtures = []
    compose = collections.OrderedDict()
    for i, name in enumerate(services, -1):
        if name == 'scoreboard':
            compose[name] = {
                'build': name,
                'ports': ['80:80', '443:443'] if use_tls else ['80:80'],
                'depends_on': ['database'],
                'volumes': ['./data/secrets:/secrets']
            }
        elif name == 'database':
            if use_vagrant:
                db_share = '/home/vagrant/database'
            else:
                db_share = './data/database'
            compose[name] = {
                'image': 'postgres',
                'volumes': [db_share + ':/var/lib/postgresql/data']
            }
        else:
            entry, port = generate_fixture(name, i)
            fixtures.append(entry)
            collect_static(name)
            if port:
                compose[name] = {
                    'build': os.path.join('challenges', name),
                    'ports': [
                        LOCALHOST + ':' + str(BASE_PORT + i) + ':' + str(port)
                    ]
                }

        # Add extra data
        if name == 'web-guestbook':
            seccomp_path = os.path.join('.', 'config', 'seccomp', 'ctf.json')
            security_options = 'seccomp:{}'.format(seccomp_path)
            compose[name]['security_opt'] = [security_options]

    with open(FIXTURES_FILE, 'w') as outfile:
        yaml.dump(fixtures, outfile)

    with open(COMPOSE_FILE, 'w') as compose_file:
        compose_file.write('version: "3.3"\n')
        yaml.dump({'services': compose}, compose_file)

    return compose


def build_nginx_config(compose, use_tls):
    """ Dynamically build nginx config from docker-compose.

    Create a location block for each challenge.

    This makes everything accessible on one port.
    """
    # Create a string template for location blocks.
    location_template = '''
    location /challenges/%(name)s/puzzle/ {
        proxy_pass http://%(server)s:%(port)d/;
    }'''

    # Create data for each nginx location block.
    sections = []
    ignore = set(['scoreboard', 'database'])
    for service, config in compose.items():
        if service not in ignore:
            port = config['ports'][0]
            external_port = int(port.split(':')[2])
            data = {'name': service, 'server': service, 'port': external_port}
            sections.append(location_template % data)

    # Read the input template.
    if use_tls:
        nginx_template = os.path.join(THIS_DIR, 'tls_nginx_template.conf')
    else:
        nginx_template = os.path.join(THIS_DIR, 'nginx_template.conf')
    with open(nginx_template) as in_fp:
       config_text = in_fp.read()

    # Format output.
    location_blocks = '\n'.join(sections)
    config_output = config_text % {'location_blocks': location_blocks}

    # Write the output config file.
    output_nginx_config = os.path.join(BASE_DIR, 'scoreboard', 'nginx.conf')
    with open(output_nginx_config, 'w') as out_fp:
       out_fp.write(config_output)


def parse_args():
    """ Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--tls', action='store_true',
                        help='use TLS for the HTTP server')
    parser.add_argument('--vagrant', action='store_true',
                        help='use Vagrant to provision the application')
    return parser.parse_args()


def main():
    """ Run the helper functions.
    """
    args = parse_args()
    use_tls = args.tls
    use_vagrant = args.vagrant
    compose = challenge_config_and_static_files(use_tls, use_vagrant)
    build_nginx_config(compose, use_tls)


if __name__ == '__main__':
    main()

