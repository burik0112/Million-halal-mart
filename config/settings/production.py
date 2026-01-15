import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from decouple import config

from config.settings.base import *

DEBUG = config("DEBUG")

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("DB_NAME"),
#         "USER": config("BOUNCER_USER"),
#         "PASSWORD": config("BOUNCER_PASSWORD"),
#         "HOST": config("BOUNCER_HOST"),
#         "PORT": config("BOUNCER_PORT"),
#     }
# }
# SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# STATIC_URL = "static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "../", "staticfiles")

# "https://688110a55be44f2eaf7b1e0c8f7549b9@o1113688.ingest.sentry.io/6144432"
sentry_sdk.init(
    dsn="https://a3fdf4caf4765a08afd9dd01c0d11f41@o4506424091934720.ingest.sentry.io/4506424100323328",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
