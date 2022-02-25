# Generated by Django 3.2.6 on 2022-02-25 19:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basic', '0009_auto_20220204_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoresult',
            name='uploaded_by',
        ),
        migrations.AddField(
            model_name='videoresult',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='image',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 25, 19, 26, 44, 129226)),
        ),
    ]
