git pull origin main
python3.8 manage.py migrate
python3.8 manage.py collectstatic
sudo systemctl start gunicorn
sudo systemctl start nginx