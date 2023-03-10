from django.core.management.base import BaseCommand
from subprocess import call


# При выполнении manage.py bot запускает handle()
class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        call(["python", '/home/sammy/myprojectdir/bot_app/management/commands/src/main.py'])
