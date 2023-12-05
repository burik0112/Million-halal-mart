import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from decouple import config

from config.settings.base import *

DEBUG = config("DEBUG")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("BOUNCER_USER"),
        "PASSWORD": config("BOUNCER_PASSWORD"),
        "HOST": config("BOUNCER_HOST"),
        "PORT": config("BOUNCER_PORT"),
    }
}


# STATIC_URL = "static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "../", "staticfiles")

# sentry_sdk.init(
#     dsn="",
#     integrations=[DjangoIntegration()],

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )
