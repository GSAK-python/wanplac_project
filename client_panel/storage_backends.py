from storages.backends.s3boto3 import S3Boto3Storage

from wanplac_project import settings

"""
StaticStorage - uncomment if u want to retrive static files for app form AWS S3, 
then go to setting and uncomment rest of setting for S3 static
"""
# class StaticStorage(S3Boto3Storage):
#     location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
