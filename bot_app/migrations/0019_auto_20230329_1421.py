# Generated by Django 3.2.5 on 2023-03-29 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0018_botbutton_open_line'),
    ]

    operations = [
        migrations.AddField(
            model_name='botbutton',
            name='num_selected',
            field=models.IntegerField(default=0, verbose_name='количество обращений'),
        ),
        migrations.AlterField(
            model_name='botuser',
            name='counter',
            field=models.IntegerField(default=0, verbose_name='количество обращений'),
        ),
    ]
