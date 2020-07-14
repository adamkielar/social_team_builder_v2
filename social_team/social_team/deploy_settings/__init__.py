import os
import dj_database_url

from social_team.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

