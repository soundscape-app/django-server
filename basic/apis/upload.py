import re
import time
import json
import numpy as np
from scipy import io
import soundfile as sf
from pydub import AudioSegment

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
        duration = round(f.frames / f.samplerate, 2)
        return duration
    except Exception as e:
        return None

def handle_uploaded_file(f, prefix):
    filename = f'audios/{prefix}_{int(time.time())}.wav'
    audio_path = 'media/'+filename
    if str(f).endswith('.m4a'):
        track = AudioSegment.from_file(f, format='m4a')
        print(audio_path)
        file_handle = track.export(audio_path, format='wav')
    elif str(f).endswith('.wav'):
        with open(audio_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    else:
        raise Exception('File type is not supported')

    duration = get_duration(audio_path)
    return filename, duration

def get_rates(file_name):
    rate, data = io.wavfile.read(f'media/{file_name}')
    sum_amp = np.sum(data)
    
    value_pn = (sum_amp / 111) % 1
    value_sn = (sum_amp / 223) % 1
    value_br = (sum_amp / 389) % 1
    value_others = (sum_amp / 599) % 1
    
    value_sum = value_pn + value_sn + value_br + value_others
    rate_pn = round(value_pn / value_sum, 2)
    rate_sn = round(value_sn / value_sum, 2)
    rate_br = round(value_br / value_sum, 2)
    rate_others = round(value_others / value_sum, 2)
    
    return [
        {'name': '폐렴', 'rate': rate_pn, 'color': '#D88024'},
        {'name': '부비동염', 'rate': rate_sn, 'color': '#D84C6F'},
        {'name': '기관지염', 'rate': rate_br, 'color': '#774AEF'},
        {'name': '기타', 'rate': rate_others, 'color': '#1767D2'},
    ]

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
        survey = data.get('survey')
        
        print(audio)
        
        file_name, duration = handle_uploaded_file(audio, prefix='cough')
        obj = Audio.objects.create(wav_file=file_name, duration=duration)
        obj.survey = json.loads(survey)
        obj.result = { 'rates': get_rates(file_name) }
        obj.save()
        
        result = { "message": "ok", "file": file_name, "audio_id": obj.audio_id, 'result': obj.result }
        print(result)
        return Response(result, status=status.HTTP_200_OK)
