from decouple import config

from vector_demonstration.settings import *  # noqa

MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

if config("CI", False):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": config("TEST_DB_NAME"),
            "USER": config("TEST_DB_USER"),
            "PASSWORD": config("TEST_DB_PASS", default=""),
            "HOST": config("DB_HOST"),
            "CONN_MAX_AGE": 600,
        },
    }
