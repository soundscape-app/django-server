from django.db import models
from django.contrib.auth.models import User


class UserSurvey(models.Model):
    id = models.BigAutoField(help_text="User Survey ID", primary_key=True)

    # TODO: 항목 추가


class TCI_RS(models.Model):
    harm_avoidance = models.CharField(help_text="Harm Avoidance", max_length=64, null=True)
    reward_dependence = models.CharField(help_text="Reward Dependence", max_length=64, null=True)
    self_directedness = models.CharField(help_text="Self Directedness", max_length=64, null=True)
    cooperativeness = models.CharField(help_text="Cooperativeness", max_length=64, null=True)
    self_transcendence = models.CharField(help_text="Self Transcendence", max_length=64, null=True)


class Profile(models.Model):
    # pw_hash = models.CharField(help_text="PW Hash", max_length=64, blank=False, null=True)
    # name = models.CharField(help_text="Name", max_length=256, blank=False, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(help_text="Name", max_length=64, blank=False, null=True)
    gender = models.CharField(help_text="Gender", max_length=32, blank=False, null=True)
    age = models.IntegerField(help_text="Age", blank=False, null=True)

    # notification_agreement = models.BooleanField(default=True, null=False)

    # user_survey_id = models.ForeignKey(UserSurvey, on_delete=models.CASCADE, null=True)
    # tci_rs_id = models.ForeignKey(TCI_RS, on_delete=models.CASCADE, null=True)
