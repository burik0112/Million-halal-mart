#!/usr/bin/env bash
# Прекратить выполнение при ошибке
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Сборка статических файлов (стили, картинки)
python manage.py collectstatic --no-input

# Применение миграций базы данных
python manage.py migrate