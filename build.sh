pip install -r webmaster/requirements.txt
pip install gunicorn
python manage.py collectstatic --no-input
python manage.py migrate