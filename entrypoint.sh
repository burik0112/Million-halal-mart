#!/usr/bin/env bash
set -e

# Выполняем миграции
python manage.py migrate --noinput

# Собираем статику
python manage.py collectstatic --noinput

# Запускаем сервер (ОБЯЗАТЕЛЬНО проверь путь к wsgi!)
exec gunicorn config.wsgi:application --bind 0.0.0.0:10000