python3 ./wait_for_database.py
python3 ./manage.py makemigrations --no-input
python3 ./manage.py migrate
python3 ./manage.py loaddata challenges
python3 ./manage.py collectstatic --no-input
uwsgi --stop site.sock
uwsgi -s site.sock --chmod-socket=664 --module scoreboard.wsgi -p 4 \
      --uid scoreboard --master --enable-threads
