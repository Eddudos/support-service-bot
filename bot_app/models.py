from django.db import models
from django.utils.timezone import now
from datetime import datetime as dt


"""
Таблицы базы данных
"""


class BotUser(models.Model):
    user_id = models.CharField(verbose_name='id пользователя', max_length=100)
    name = models.CharField(verbose_name='имя пользователя', max_length=100, null=True, blank=True)
    initial_date = models.DateTimeField(verbose_name='дата первого обращения', default=now)
    last_date = models.DateTimeField(verbose_name='дата последнего обращения', default=now)
    counter = models.IntegerField(verbose_name='количество обращений', default=1)

    def __str__(self):
        return str(self.name)


class BotDictionary(models.Model):
    name = models.CharField(verbose_name='имя текста', max_length=200)
    value = models.TextField(verbose_name='текст')

    def __str__(self):
        return self.name


class BotButton(models.Model):
    name = models.CharField(verbose_name='текст кнопки', max_length=200)
    # num_btns = models.IntegerField()
    reaction = models.TextField(verbose_name='реакция')

    def __str__(self):
        return self.name

class BotClient(models.Model):
    name = models.CharField(verbose_name='наименование университета', max_length=200, unique=True)
    activity = models.BooleanField(verbose_name='activity')

    def __str__(self):
        return self.name

class TokenTable(models.Model):
    name = models.CharField(verbose_name='Token type', max_length=200, unique=True)
    token = models.CharField(verbose_name='access_token', max_length=255)
    # refresh_token = models.CharField(verbose_name='refresh_token', max_length=255)

    def __str__(self):
        return self.name