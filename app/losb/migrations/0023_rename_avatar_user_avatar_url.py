# Generated by Django 5.1.2 on 2024-10-25 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('losb', '0022_rename_bday_user_birthday_rename_city_user_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='avatar',
            new_name='avatar_url',
        ),
    ]