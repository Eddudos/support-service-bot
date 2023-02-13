import sys
from asgiref.sync import sync_to_async

sys.path.append('C:\\Users\\user\\Documents\\TeleBot\\pet_projects\\bot_project\\germ-bot\\germ-bot')

from django.apps import apps
from django.conf import settings
from django.utils.timezone import now

settings.configure(INSTALLED_APPS=['bot_app'], DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }}
)

apps.populate(settings.INSTALLED_APPS)
from bot_app.models import BotUser, BotButton, BotClient, BotDictionary
from django.db.models import F


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
def update_field(table, query):
    if table == BotUser:
        table.objects.filter(name=query).update(last_date=now(), counter=F('counter')+1)
