import logging
from datetime import datetime, timedelta

from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status

from basic.models.prediction import Prediction
from basic.models.media import VideoResult

import requests
import json
import math

def result_serializer(video):
    results = dict()
    results['video_id'] = video.video_id
    results['prediction'] = video.prediction
    results['revisitation'] = video.revisitation
    results['loudness'] = video.loudness
    if video.json_data:
        results['video_data'] = json.loads(video.json_data)
    else:
        results['video_data'] = {}
    results['uploaded_at'] = video.created_datetime
    results['predicted_at'] = video.updated_datetime
    results['status'] = video.status
    return results
