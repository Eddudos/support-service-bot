import sys
from asgiref.sync import sync_to_async

sys.path.append('/home/sammy/myprojectdir')

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
    }
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
    if table == BotDictionary:
        return table.objects.get(name=query).value
    elif table == BotButton:
        return [(button.name, button.reaction) for button in BotButton.objects.all()]
    elif table == TokenTable:
        return table.objects.get(name=query).token


# Проверка начличия в базе
@sync_to_async
def check_if_exists(table, query):
    if table == BotUser:
        return table.objects.filter(name=query).exists()
    elif table == BotClient:
        if table.objects.filter(name=query).exists():
            return table.objects.get(name=query).activity


# Обновление поля в базе
@sync_to_async
def update_field(table, query, token=''):
    if table == BotUser:
        table.objects.filter(name=query).update(last_date=now(), counter=F('counter')+1)
    if table == TokenTable:
        table.objects.filter(name=query).update(token=token)







