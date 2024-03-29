# Generated by Django 3.2.6 on 2022-03-18 10:42

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('date_uploaded', models.DateTimeField(default=datetime.datetime(2022, 3, 18, 10, 42, 41, 971926))),
            ],
        ),
        migrations.CreateModel(
            name='SiteAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('l_aeq', models.FloatField()),
                ('l_ceq', models.FloatField()),
                ('green_ratio', models.FloatField()),
                ('grey_ratio', models.FloatField()),
                ('sky_ratio', models.FloatField()),
                ('people_count', models.IntegerField()),
                ('vehicle_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SiteSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loudness', models.FloatField(help_text='Loudness')),
                ('revisitation', models.FloatField(help_text='Revisitation')),
            ],
        ),
        migrations.CreateModel(
            name='TCI_RS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('harm_avoidance', models.CharField(help_text='Harm Avoidance', max_length=64, null=True)),
                ('reward_dependence', models.CharField(help_text='Reward Dependence', max_length=64, null=True)),
                ('self_directedness', models.CharField(help_text='Self Directedness', max_length=64, null=True)),
                ('cooperativeness', models.CharField(help_text='Cooperativeness', max_length=64, null=True)),
                ('self_transcendence', models.CharField(help_text='Self Transcendence', max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSurvey',
            fields=[
                ('id', models.BigAutoField(help_text='User Survey ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='VideoResult',
            fields=[
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='생성일시')),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True, verbose_name='수정일시')),
                ('video_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('video', models.FileField(null=True, upload_to='videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('loudness', models.FloatField(blank=True, null=True)),
                ('revisitation', models.FloatField(blank=True, null=True)),
                ('device', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(default='ready', max_length=30)),
                ('json_data', models.TextField(default=None, null=True)),
                ('prediction', models.FloatField(default=None, null=True)),
                ('survey', models.JSONField(default=None, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('media_url', models.URLField()),
                ('site_analysis_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.siteanalysis')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=64, null=True)),
                ('gender', models.CharField(help_text='Gender', max_length=32, null=True)),
                ('age', models.IntegerField(help_text='Age', null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('value', models.FloatField()),
                ('site_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.site')),
                ('site_survey_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.sitesurvey')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.profile')),
            ],
        ),
    ]
