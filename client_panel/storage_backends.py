from storages.backends.s3boto3 import S3Boto3Storage

from wanplac_project import settings


# class StaticStorage(S3Boto3Storage):
#     location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
