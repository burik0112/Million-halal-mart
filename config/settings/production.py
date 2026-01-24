from config.settings.base import *
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
#
# DEBUG = False # В продакшене ОБЯЗАТЕЛЬНО False
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    SECURE_SSL_REDIRECT = False

sentry_sdk.init(
    dsn="https://a3fdf4caf4765a08afd9dd01c0d11f41@o4506424091934720.ingest.sentry.io/4506424100323328",
    integrations=[DjangoIntegration()],
    # ...
)