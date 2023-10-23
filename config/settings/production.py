import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from config.settings.base import *

DEBUG = False

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