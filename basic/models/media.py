import json

from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

from backend.models import TimeStampedModel

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/',blank=True, null=True)
    date_uploaded = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.title

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
    
    # @property
    # def json_dict(self):
    #     return json.loads(self.json_data)
