pip install -r webmaster/requirements.txt
pip install gunicorn
python webmaster/manage.py collectstatic --no-input
python webmastermanage.py migrate
