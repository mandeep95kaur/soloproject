# Generated by Django 2.2 on 2021-11-07 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taste_app', '0004_auto_20211106_1221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]