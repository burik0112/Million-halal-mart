from config.settings.base import *
import dj_database_url

DEBUG = False # В продакшене всегда False!

# Проверяем наличие DATABASE_URL
DATABASE_URL = config("DATABASE_URL", default=None)

if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600, 
        ssl_require=True
    )

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Настройки Sentry остаются...
sentry_sdk.init(
    dsn="твой_dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)