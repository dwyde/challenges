python3 ./wait_for_database.py
python3 ./manage.py makemigrations challenges --no-input
python3 ./manage.py migrate
python3 ./manage.py loaddata challenges
#python3 ./manage.py runserver 0.0.0.0:9000
python3 ./manage.py collectstatic --no-input
uwsgi --stop site.sock
uwsgi -s site.sock --chmod-socket=664 --module scoreboard.wsgi -p 2 \
      --uid scoreboard --master --enable-threads

