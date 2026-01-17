from config.settings.base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False # В продакшене ОБЯЗАТЕЛЬНО False

# Настройки безопасности для Render (HTTPS)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True

sentry_sdk.init(
    dsn="твой_dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)