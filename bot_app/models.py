import threading as th
import time

from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# from datetime import datetime
# from datetime import timedelta
# from datetime import timezone
# from aiogram.types import InputFile
from time import sleep
from multiprocessing import Process
# import bot_app.views
# from bot_app.management.commands.src.bot_conf.app import dp, bot, broadcaster
# from aiogram.utils import executor  


"""
Таблицы базы данных
"""

# 2023-03-22 12:17:48.272376
class BotUser(models.Model):
    user_id = models.IntegerField(verbose_name='id пользователя')
    name = models.CharField(verbose_name='имя пользователя', max_length=100, null=True, blank=True)
    initial_date = models.DateTimeField(verbose_name='дата первого обращения', default=now) # input_formats=['%y-%m-%d %H:%M']
    last_date = models.DateTimeField(verbose_name='дата последнего обращения', default=now)  # auto_now=True
    counter = models.IntegerField(verbose_name='количество обращений', default=0)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        if self.name:
            return str(self.name)
        else: 
            return str(self.user_id)


class BotDictionary(models.Model):
    name = models.CharField(verbose_name='имя текста', max_length=200)
    value = models.TextField(verbose_name='текст')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Словарь'
        verbose_name_plural = 'Словарь'


class BotButton(models.Model):
    sort_id = models.IntegerField(verbose_name='сортировка', default=0)
    name = models.CharField(verbose_name='текст кнопки', max_length=200)
    # num_btns = models.IntegerField()
    reaction = models.TextField(verbose_name='реакция')
    open_line = models.BooleanField(verbose_name='открытая линия', default=False)
    num_selected = models.IntegerField(verbose_name='количество обращений', default=0)

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
    def count_num_users():
        return BotUser.objects.count()

    name = models.CharField(verbose_name='Название', max_length=200, unique=True)
    image = models.ImageField(verbose_name='Картинка', upload_to='static/telegram_img', blank=True)
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(verbose_name='Дата')
    status = models.CharField(verbose_name='Статус', max_length=13, default='запланирована')
    num_users =  models.IntegerField(verbose_name='Количество потенциальных получателей', default=count_num_users)
    num_sent = models.IntegerField(verbose_name='Количество отправок', default=0)

    # def save(self, *args, **kwargs):
    #     self.num_users = BotUser.objects.count()
    #     super(PublicationTable, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


@receiver(post_save, sender=PublicationTable)
def check_signal(sender, instance, created, **kwargs):
    from bot_app.management.commands.src.bot_conf.app import broadcaster, loop, send_photo  # start_broadcasting

    def delayed(function, delay, users, pub_message, image):
        timer = th.Timer(delay, function, kwargs={"delay": delay, 
                                                    "users": users, 
                                                    "pub_message": pub_message,
                                                    "image": image})
        timer.start()
        # process = Process(target=function, kwargs={"delay": delay, 
        #                                             "users": users, 
        #                                             "pub_message": pub_message,
        #                                             "image": image})                       
        # process.start()

    def broadcast(delay, users, pub_message, image):
        start_time = time.time()
        sleep(delay)
        print("--- %s seconds ---" % (time.time() - start_time), flush=True)
        count = loop.run_until_complete(broadcaster(users, pub_message, image))
        PublicationTable.objects.filter(name=instance).update(num_sent=count, status='отправлена')

        # if image:
        #     for user in users:
        #         with open(image.image.path, 'rb') as image_file:
        #             input_file = InputFile(image_file)
        #             loop.run_until_complete(broadcaster(user, pub_message, input_file))
        # else: 
        #     for user in users:
        #         loop.run_until_complete(broadcaster(user, pub_message, image))

    now = timezone.now()
    run_at = sender.objects.get(name=instance).date
    delay = (run_at - now).total_seconds()
    print('delay', delay)


    img = not PublicationTable.objects.filter(name=instance, image='').exists()

    tuple_users = tuple(BotUser.objects.values_list('user_id', flat=True))
    pub_message = PublicationTable.objects.get(name=instance).text

    if img:
        image = PublicationTable.objects.get(name=instance)
        delayed(broadcast, delay, tuple_users, pub_message, image)
    else: 
        delayed(broadcast, delay, tuple_users, pub_message, img)

    print('опана отправили')
