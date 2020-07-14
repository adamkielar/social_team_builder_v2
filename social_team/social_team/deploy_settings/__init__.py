import dj_database_url

from social_team.settings import *

S3_STORAGE_BACKEND = bool(int(os.environ.get('S3_STORAGE_BACKEND', 1)))
if S3_STORAGE_BACKEND is True:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_DEFAULT_ACL = 'public-read'
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('S3_STORAGE_BUCKET_REGION', 'us-east-1')
AWS_QUERYSTRING_AUTH = False

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
