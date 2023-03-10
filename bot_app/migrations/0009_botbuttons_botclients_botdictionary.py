# Generated by Django 3.2.5 on 2023-02-08 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0008_remove_botusers_chat_msg'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotButtons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('text', models.TextField(verbose_name='value')),
            ],
        ),
        migrations.CreateModel(
            name='BotClients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('activity', models.BooleanField(verbose_name='activity')),
            ],
        ),
        migrations.CreateModel(
            name='BotDictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('value', models.TextField(verbose_name='value')),
            ],
        ),
    ]
