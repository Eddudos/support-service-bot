# Generated by Django 3.2.5 on 2023-02-10 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0012_auto_20230209_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botbutton',
            name='btns',
            field=models.JSONField(verbose_name='btns'),
        ),
    ]
