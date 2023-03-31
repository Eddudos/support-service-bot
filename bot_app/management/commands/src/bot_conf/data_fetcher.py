import sys
from asgiref.sync import sync_to_async

sys.path.append('/home/sammy/myprojectdir')

from datetime import datetime as dt
from django.apps import apps
from django.conf import settings
from django.utils.timezone import now


if not settings.configured:
    settings.configure(INSTALLED_APPS=['bot_app', 'myproject'], DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'myproject',
            'USER': 'sammy',
            'PASSWORD': 'h8d44fn0.DB',
            'HOST': 'localhost',
            'PORT': '',
        }
    },
    TIME_INPUT_FORMATS = [
    '%H:%M:%S',     # '14:30:59'
    '%H:%M',        # '14:30'
    ],
    LANGUAGE_CODE = 'ru-RU',
    TIME_ZONE = 'Asia/Novosibirsk',
    # USE_I18N = True,
    USE_L10N = True,
    USE_TZ = True
    )

    apps.populate(settings.INSTALLED_APPS)

from bot_app.models import BotUser, BotButton, BotClient, BotDictionary, TokenTable
from django.db.models import F
from myproject.settings import CLIENT_ID, CLIENT_SECRET, CLIEND_ENDPOINT


"""
Файл для обращений к базе данных
"""

# Добавление в базу
@sync_to_async
def write_to_db(table, user_id, username):
    # date1 = '2020-09-17T10:05'
    # startdate = datetime.strptime(date1, "%Y-%m-%dT%H:%M")
    table.objects.create(user_id=user_id, name=username)


# Чтение из базы
@sync_to_async
def read_from_db(table, query=None):
    if table == BotUser:
        return table.objects.get(user_id=query).counter
    elif table == BotDictionary:
        return table.objects.get(name=query).value
    elif table == BotButton:
        return [(button.name, button.reaction, button.open_line) for button in BotButton.objects.all().order_by('sort_id')]
    elif table == TokenTable:
        return table.objects.get(name=query).token


# Проверка начличия в базе
@sync_to_async
def check_if_exists(table, query):
    if table == BotUser:
        return table.objects.filter(user_id=query).exists()
    elif table == BotClient:
        if table.objects.filter(name__iexact=query).exists():
            return table.objects.get(name__iexact=query).activity


# Обновление поля в базе
@sync_to_async
def update_field(table, query, token=''):
    if table == BotUser:
        table.objects.filter(user_id=query).update(last_date=now(), counter=F('counter')+1)
    elif table == TokenTable:
        table.objects.filter(name=query).update(token=token)
    elif table == BotButton:
        table = table.objects.filter(name=query).update(num_selected=F('num_selected')+1)







