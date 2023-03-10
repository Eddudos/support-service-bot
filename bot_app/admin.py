from django.contrib import admin

from . import models


# Регистрация таблиц в админке для возможности редактирования
admin.site.register([models.BotUser, models.BotButton, models.BotClient, models.BotDictionary, models.TokenTable])
