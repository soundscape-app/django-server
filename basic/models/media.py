import json

from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

from backend.models import TimeStampedModel

class VideoResult(TimeStampedModel):
    video_id = models.AutoField(primary_key=True, db_index=True)
    # title = models.CharField(max_length=200, blank=True, null=True)
    video = models.FileField(
        upload_to='videos/',
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])]
    )
    loudness = models.FloatField(blank=True, null=True)
    revisitation = models.FloatField(blank=True, null=True)
    device = models.CharField(max_length=200, blank=True, null=True)
    
    status = models.CharField(max_length=30, default='ready')
    json_data = models.TextField(default=None, null=True)
    
    prediction = models.FloatField(default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    survey = models.JSONField(default=None, null=True)
    scape_name = models.CharField(max_length=100, default=None, null=True)
    
    # @property
    # def json_dict(self):
    #     return json.loads(self.json_data)

class Audio(TimeStampedModel):
    audio_id = models.AutoField(primary_key=True, db_index=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    wav_file = models.FileField(
        upload_to='audio/',
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['wav'])]
    )
    duration = models.FloatField(blank=True, null=True)
    survey = models.JSONField(null=True)