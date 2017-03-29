python3 ./manage.py makemigrations challenges
python3 ./manage.py migrate
python3 ./manage.py loaddata challenges
python3 ./manage.py runserver 0.0.0.0:9000
