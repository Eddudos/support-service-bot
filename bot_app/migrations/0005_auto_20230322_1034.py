# Generated by Django 3.2.5 on 2023-03-22 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0004_auto_20230307_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Token type')),
                ('image', models.ImageField(blank=True, upload_to='static/telegram_img')),
                ('text', models.TextField()),
                ('date', models.DateTimeField()),
                ('status', models.CharField(choices=[('запланирована', 'запланирована'), ('отправлена', 'отправлена')], max_length=13)),
                ('num_users', models.IntegerField(default=1, editable=False)),
            ],
            options={
                'verbose_name': 'Публикация',
                'verbose_name_plural': 'Публикации',
            },
        ),
        migrations.AlterModelOptions(
            name='botbutton',
            options={'verbose_name': 'Тип обращений', 'verbose_name_plural': 'Типы обращений'},
        ),
        migrations.AlterModelOptions(
            name='botclient',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='botdictionary',
            options={'verbose_name': 'Словарь', 'verbose_name_plural': 'Словарь'},
        ),
        migrations.AlterModelOptions(
            name='botuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
