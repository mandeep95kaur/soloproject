# Generated by Django 2.2 on 2021-11-17 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taste_app', '0015_remove_review_customer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]