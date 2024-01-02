pkill -f "gunicorn"

gunicorn --bind 0.0.0.0:8012 tulsi_laser_tech.wsgi --daemon