# Generated by Django 3.2.5 on 2023-03-24 15:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0012_auto_20230324_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botuser',
            name='initial_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата первого обращения'),
        ),
        migrations.AlterField(
            model_name='botuser',
            name='last_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата последнего обращения'),
        ),
    ]
