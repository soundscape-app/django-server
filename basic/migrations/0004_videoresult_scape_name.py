# Generated by Django 3.2.6 on 2022-03-18 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_delete_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoresult',
            name='scape_name',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]