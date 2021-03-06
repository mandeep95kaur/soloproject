# Generated by Django 2.2 on 2021-11-17 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taste_app', '0010_delete_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('rating', models.IntegerField()),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('creater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_created_review', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taste_app.Customer')),
                ('review_by', models.ManyToManyField(related_name='reviewer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
