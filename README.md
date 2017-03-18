# Capture The Flag (CTF) Challenges
This repo contains standalone software puzzles, some of which are security-themed.

For instructions on how to set up and access the simple dashboard, please see
below.

Some of the challenges are intended to be solved without reading the source.
Everything you need should be in the dashboard.

## Setup
1. Install Python 3, pip, and Docker
1. `pip3 install --upgrade docker-compose pyyaml`
1. `sudo ./run.sh # sudo or add yourself to the docker group...`
1. Browse to port 9000 on your Docker IP (e.g., http://172.17.0.1:9000/)

Tested on Arch Linux with Python 3.6

**NOTE:** Ubuntu's `pip` puts docker-compose in `~/.local/bin/docker-compose`.
You'll want to do `sudo ~/.local/bin/docker-compose up -d --build` instead
of `./run.sh`.

## Automatic Authentication
Your user is automatically created and its session saved in a cookie.
If your cookie gets deleted, a new user will be created for you.

## Administration
To grant access to Django's admin interface, you can provide user IDs
in the scoreboard Docker container:

1. `docker-compose exec scoreboard bash`
1. `python3 manage.py grant_admin 1 2 3 # User ID's of admins`
1. Browse to /admin/ on the scoreboard (e.g., http://172.17.0.1:9000/admin/)

## Development
If you change challenge metadata, please run `config/prepare_scoreboard.py`.
This collects static files and database entries for the scoreboard.

Then, you can do `./run.sh` as normal.

## To-do
- Persistent storage: the challenge database gets wiped out on every rebuild
- A real Django setup (nginx in front of gunicorn, etc.)
- Add write-ups and tests?
- Multi-user support in the scoreboard
