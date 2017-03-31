python3 ./wait_for_database.py
python3 ./manage.py makemigrations challenges
python3 ./manage.py migrate
python3 ./manage.py loaddata challenges
#python3 ./manage.py runserver 0.0.0.0:9000
python3 ./manage.py collectstatic --no-input
uwsgi -s :8001 --module scoreboard.wsgi
