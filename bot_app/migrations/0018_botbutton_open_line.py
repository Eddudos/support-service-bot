# Generated by Django 3.2.5 on 2023-03-27 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0017_botbutton_sort_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='botbutton',
            name='open_line',
            field=models.BooleanField(default=False, verbose_name='открытая линия'),
        ),
    ]
