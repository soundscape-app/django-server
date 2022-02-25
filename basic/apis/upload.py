import logging
from datetime import datetime, timedelta

from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status

from basic.models.prediction import Prediction
from basic.models.media import VideoResult
from backend.decorators import parse_header

class UploadViewSet(viewsets.ViewSet):
    http_method_names = ["post", "get"]
    
    @action(detail=False, methods=['POST'])
    @method_decorator(parse_header())
    def video(self, request):
        data = request.data
        
        user = None
        if request.user:
            user = request.user

        device_model = None
        try:
            device_model = request.device_model
        except:
            pass
        
        video = data.get('video')
        revisitation = float(data.get('revisitation', 0))
        loudness = float(data.get('loudness', 0))
        device = str(data.get('device', 'unknown'))
        
        if not video:
            return Response({"message": "Video is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        video_result = VideoResult.objects.create(
            video=video,
            revisitation=revisitation,
            loudness=loudness,
            device=device,
            user=user,
        )
        video_result.status = 'uploaded'
        video_result.save()
        
        res = dict()
        res['video_id'] = video_result.video_id
        res['user_id'] = user.id
        res['revisitation'] = revisitation
        res['loudness'] = loudness
        res['device'] = device
        res['device_model'] = device_model
        res['uploaded_at'] = video_result.created_datetime

        return Response(res, status=status.HTTP_200_OK)
