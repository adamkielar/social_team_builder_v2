import os
import dj_database_url

from social_team.settings import *

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DEBUG = bool(int(os.environ.get('DEBUG', 0)))

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_SANDBOX_MODE_IN_DEBUG=False

S3_STORAGE_BACKEND = bool(int(os.environ.get('S3_STORAGE_BACKEND', 1)))
if S3_STORAGE_BACKEND is True:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_DEFAULT_ACL = 'public-read'
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('S3_STORAGE_BUCKET_REGION', 'us-east-1')
AWS_QUERYSTRING_AUTH = False

