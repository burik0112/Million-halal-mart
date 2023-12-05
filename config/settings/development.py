from config.settings.base import *
from decouple import config


DEBUG = config("DEBUG")

# STATIC_URL = "static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "../", "staticfiles")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USERNAME"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOSTNAME"),
        "PORT": config("DB_PORT"),
    }
}
