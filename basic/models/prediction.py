from django.db import models

from basic.models.profile import Profile
from basic.models.site import Site


class SiteSurvey(models.Model):
    loudness = models.FloatField(help_text="Loudness")
    revisitation = models.FloatField(help_text="Revisitation")
    # TODO: 정확한 자료형 설정 필요


class Prediction(models.Model):
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    site_survey_id = models.ForeignKey(SiteSurvey, on_delete=models.CASCADE, null=True)

    created = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()



