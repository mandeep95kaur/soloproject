# Generated by Django 2.2 on 2021-11-17 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taste_app', '0017_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='customer',
        ),
    ]
