# Generated by Django 3.2.5 on 2023-02-10 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0015_alter_botbutton_btns'),
    ]

    operations = [
        migrations.RenameField(
            model_name='botuser',
            old_name='username',
            new_name='name',
        ),
    ]