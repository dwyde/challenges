import json
import os.path

import requests


# A URL from which to download Docker's default seccomp config
SECCOMP_DEFAULT_URL = ('https://github.com/docker/engine/'
                       'raw/master/profiles/seccomp/default.json')


def main():
    entry = {
        'names': ['clone', 'unshare'],
        'action': 'SCMP_ACT_ALLOW',
        'args': [],
        'comment': '',
        'includes': {},
        'excludes': {}
    }

    response = requests.get(SECCOMP_DEFAULT_URL)
    data = json.loads(response.text)
    data['syscalls'].append(entry)

    outfile = os.path.join(os.path.dirname(__file__), 'ctf.json')
    with open(outfile, 'w') as fp:
        json.dump(data, fp, separators=(',', ':'))


if __name__ == '__main__':
    main()

