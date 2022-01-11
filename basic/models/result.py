from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

from backend.models import TimeStampedModel

class Result(TimeStampedModel):
    video_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=30, default='ready')
    json = models.TextField(default=None, null=True)



    
