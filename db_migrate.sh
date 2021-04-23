python manage.py db init;
python manage.py db migrate --message "$1";
python manage.py db upgrade;
