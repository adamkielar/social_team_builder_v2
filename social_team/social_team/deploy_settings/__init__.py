import os
import dj_database_url

from social_team.settings import *

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DEBUG = bool(int(os.environ.get('DEBUG', 0)))

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
