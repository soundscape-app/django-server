# Generated by Django 3.2.6 on 2021-12-03 12:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('date_uploaded', models.DateTimeField(default=datetime.datetime(2021, 12, 3, 12, 31, 26, 217552))),
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
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pw_hash', models.CharField(help_text='PW Hash', max_length=64, null=True)),
                ('name', models.CharField(help_text='Name', max_length=256, null=True)),
                ('gender', models.CharField(help_text='Gender', max_length=32, null=True)),
                ('age', models.IntegerField(help_text='Age', null=True)),
                ('notification_agreement', models.BooleanField(default=True)),
                ('tci_rs_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.tci_rs')),
                ('user_survey_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.usersurvey')),
            ],
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
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('value', models.FloatField()),
                ('site_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.site')),
                ('site_survey_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.sitesurvey')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.user')),
            ],
        ),
    ]
