# Generated by Django 3.2.6 on 2022-04-21 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0005_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
