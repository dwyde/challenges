# Under The CTF
This code runs at https://underthectf.com.

# Capture The Flag (CTF) Challenges
This repository contains standalone software puzzles, some of which are security-themed.

For instructions on how to set up and access the simple dashboard, please see
below.

Some of the challenges are intended to be solved without reading the source.
Everything you need should be in the dashboard.

## Setup
1. Install Python 3, pip, and Docker: `apt install python3-pip docker.io`.
1. `pip3 install --upgrade docker-compose pyyaml`
1. `sudo ./run.sh # sudo, or add yourself to the "docker" group`
1. Wait for the Docker containers to build.
1. Browse to http://localhost/.

Tested on Ubuntu 18.04 with Python 3.6.

## Automatic Authentication
A session is automatically created and stored in a cookie.
If your cookie is deleted, a new session will be created for you.

## Development
If you change challenge metadata, please run `python3 config/prepare_scoreboard.py`.
This collects static files and database entries for the scoreboard.

Then, you can do `./run.sh` as normal.

Run `python3 config/prepare_scoreboard.py --tls` to configure
HTTPS for the web server. Place the certificate chain at
`scoreboard/under-the-ctf.chain` and the key at 
`scoreboard/under-the-ctf.key`.

