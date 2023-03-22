from django.db import models
from django.utils.timezone import now
from datetime import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver


"""
Таблицы базы данных
"""

class BotUser(models.Model):
    user_id = models.CharField(verbose_name='id пользователя', max_length=100)
    name = models.CharField(verbose_name='имя пользователя', max_length=100, null=True, blank=True)
    initial_date = models.DateTimeField(verbose_name='дата первого обращения', default=now)
    last_date = models.DateTimeField(verbose_name='дата последнего обращения', default=now)
    counter = models.IntegerField(verbose_name='количество обращений', default=1)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.name)


class BotDictionary(models.Model):
    name = models.CharField(verbose_name='имя текста', max_length=200)
    value = models.TextField(verbose_name='текст')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Словарь'
        verbose_name_plural = 'Словарь'


class BotButton(models.Model):
    name = models.CharField(verbose_name='текст кнопки', max_length=200)
    # num_btns = models.IntegerField()
    reaction = models.TextField(verbose_name='реакция')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип обращений'
        verbose_name_plural = 'Типы обращений'


class BotClient(models.Model):
    name = models.CharField(verbose_name='наименование университета', max_length=200, unique=True)
    activity = models.BooleanField(verbose_name='activity')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class TokenTable(models.Model):
    name = models.CharField(verbose_name='Token type', max_length=200, unique=True)
    token = models.CharField(verbose_name='access_token', max_length=255)
    # refresh_token = models.CharField(verbose_name='refresh_token', max_length=255)

    def __str__(self):
        return self.name


class PublicationTable(models.Model):
    STATUSES = (
        ('запланирована', 'запланирована'),
        ('отправлена', 'отправлена')
    )

    name = models.CharField(verbose_name='Название', max_length=200, unique=True)
    image = models.ImageField(verbose_name='Картинка', upload_to='static/telegram_img', blank=True)
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(verbose_name='Дата')
    status = models.CharField(verbose_name='Статус', max_length=13, choices=STATUSES)
    num_users =  models.IntegerField(verbose_name='Количество отправок', default=BotUser.objects.all().count())


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

@receiver(post_save, sender=BotDictionary)
def check_signal(sender, instance, created, **kwargs):
    print("Hello from signal handler")
    print(sender)
    print(instance.value)
    print(created)
