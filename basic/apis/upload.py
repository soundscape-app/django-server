import logging
from datetime import datetime, timedelta
import json
import time
import soundfile as sf

from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status

from basic.models.prediction import Prediction
from basic.models.media import VideoResult, Audio
from backend.decorators import parse_header

# utils

def get_duration(audio_path):
    try:
        f = sf.SoundFile(audio_path)
        duration = f.frames / f.samplerate
        return duration
    except Exception as e:
        return None

def handle_uploaded_file(f, prefix):
    filename = f'audios/{prefix}_{int(time.time())}.wav'
    audio_path = 'media/'+filename
    with open(audio_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    duration = get_duration(audio_path)
    return filename, duration

@permission_classes((AllowAny,))
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
        survey = json.loads(data.get('survey','{}'))
        scape_name = str(survey.get('name', '(none)'))
        
        if not video:
            return Response({"message": "Video is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        video_result = VideoResult.objects.create(
            video=video,
            revisitation=revisitation,
            loudness=loudness,
            device=device,
            user=user,
            survey=survey,
            scape_name=scape_name,
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
    
    
    @action(detail=False, methods=['POST'])
    def audio(self, request):
        data = request.data
        audio = data.get('audio')
        
        file_name, duration = handle_uploaded_file(audio, prefix='cough')
        Audio.objects.create(wav_file=file_name, duration=duration)
            
        result = { "message": "ok", "file": file_name }
        return Response(result, status=status.HTTP_200_OK)
