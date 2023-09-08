from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.PRIVATE_MEDIAFILES_LOCATION
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
