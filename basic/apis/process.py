import logging
from datetime import datetime, timedelta

from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework import viewsets, status

from basic.models.prediction import Prediction
from basic.models.media import VideoResult
from basic.utils.result_serializer import result_serializer

import requests
import json
import math

# def get_prediction_data(video):

def proc(video):
    URL = 'http://api-server-1507785389.ap-northeast-2.elb.amazonaws.com:4040/process'
    response = requests.post(URL, files={'video': video.video.file})
    res = json.loads(''.join(response.content.decode('utf-8')))
    return res

def luminance(data):
    CF = {
        'r': 0.299,
        'g': 0.587,
        'b': 0.114,
    }
    CONST = 0
    result = sum([CF[key] * data[key] for key in CF.keys()]) + CONST
    return result

def loudness(data):
    CF = {
        'laeq': 0.091,
        'sky_ratio': -0.044,
        'luminance': 0.014,
        'n_ppl': -0.019,
        'n_vhcl': 0.007,
        'grey_ratio': 0.012,
    }
    CONST = -4.686
    result = sum([CF[key] * data[key] for key in CF.keys()]) + CONST
    return result

def revisitation(data):
    CF = {
        'lceq-laeq': -0.063,
        'sky_ratio': 0.019,
        'n_ppl': 0.012,
        'n_vhcl': -0.008,
        'grey_ratio': -0.023,
    }
    CONST = 3.931
    result = sum([CF[key] * data[key] for key in CF.keys()]) + CONST
    return result

def predict(data):
    CF = {
        'laeq': 0.051,
        'lceq-laeq': -0.166,
        'green_ratio': 0.058,
        'n_ppl': -0.031,
        'n_vhcl': -0.018,
        'loudness': -0.57,
        'revisitation': 0.815,
    }
    CONST = -1.568
    
    result = sum([CF[key] * data[key] for key in CF.keys()]) + CONST
    exp_result = math.exp(result)
    percent = exp_result / (1 + exp_result)
    return percent

class ProcessViewSet(viewsets.ViewSet):
    http_method_names = ["post", "get"]

    @action(detail=False, methods=['GET'])
    def video(self, request, *args, **kwargs):
        """video id로 요청하면 결과 가져옴"""
        
        video_id = request.query_params.get('video_id', None)
        redo = request.query_params.get('redo', False)
        video = VideoResult.objects.get(video_id=video_id)
        video.status = 'processing';
        video.save()
        
        if not redo and video.json_data:
            proc_data = json.loads(video.json_data)
        else:
            proc_data = proc(video)
            video.json_data = json.dumps(proc_data)
            video.save()
        
        data = dict()
        
        # Divice
        data['device'] = video.device
        if video.device and video.device.startswith('Apple'):
            pass
            # TODO: 오디오 파일 분석 후 조정 필요
        
        # Luminance
        data['r'] = proc_data['rgb_info']['r']['avg']
        data['g'] = proc_data['rgb_info']['g']['avg']
        data['b'] = proc_data['rgb_info']['b']['avg']
        data['luminance'] = luminance(data)
        
        # Sound Info
        data['lceq'] = proc_data['audio']['leq']
        data['laeq'] = proc_data['audio']['laeq']
        data['lceq-laeq'] = proc_data['audio']['lceq-laeq']
        
        # Image Segmentation TODO: grey ratio 는 이게 맞는지
        data['sky_ratio'] = proc_data['segment']['Sky']
        data['green_ratio'] = proc_data['segment']['Green']
        # data['grey_ratio'] = proc_data['segment']['Grey']
        data['grey_ratio'] = 1 - data['sky_ratio'] - data['green_ratio']
        
        # Counting
        data['n_ppl'] = proc_data['yolo']['person']
        data['n_vhcl'] = proc_data['yolo']['vehicle']
    
        # Survey Data
        if video.loudness == 0:
            video.loudness = loudness(data)
        if video.revisitation == 0:
            video.revisitation = revisitation(data)
        video.save()
        
        data['loudness'] = video.loudness
        data['revisitation'] = video.revisitation
        
        video.prediction = predict(data)
        video.status = 'processed';
        video.save()
        
        # results = dict()
        # results['video_id'] = video.video_id
        # results['prediction'] = video.prediction
        # results['revisitation'] = video.revisitation
        # results['loudness'] = video.loudness
        # results['video_data'] = proc_data
        # results['uploaded_at'] = video.created_datetime
        # results['predicted_at'] = video.updated_datetime
        
        results = result_serializer(video)

        return Response(results, status=status.HTTP_200_OK)

    # @method_decorator(parse_header())
    # @action(detail=False, methods=['GET'])
    def list(self, request, *args, **kwargs):
        """모든 예측 영상 항목을 가져옵니다 TODO: 유저 별 구분 필요"""
        # clayful_customer_id = None
        # if request.customer:
        #     clayful_customer_id = request.customer.clayful_customer_id

        # page_size = int(request.query_params.get('page_size', 50))
        # keyword = request.query_params.get('keyword', None)
        
        # request.query_params.get('redo', False)

        # queryset = VideoResult.objects.filter(
        #     uploaded_by=request.user
        # )
        
        queryset = VideoResult.objects.filter(
            created_datetime__gte=datetime.now() - timedelta(hours=12),
            video__isnull=False
        )
        
        # if keyword:
        #     keyword = keyword.lower()
        #     queryset = queryset.filter(search_text__contains=keyword)

        # queryset = queryset.order_by('-created_datetime')
        # queryset = queryset[:page_size]

        results = []
        for video in queryset:
            data = result_serializer(video)
            results.append(data)
        results = results[50::-1]

        return Response(results, status=status.HTTP_200_OK)

#  res = dict({
#         "rgb_info": {
#             "b": {
#                 "avg": 154.2338254026956,
#                 "max": 255.0,
#                 "med": 154.0,
#                 "min": 0.0
#             },
#             "g": {
#                 "avg": 150.32975324621958,
#                 "max": 255.0,
#                 "med": 159.0,
#                 "min": 1.5
#             },
#             "r": {
#                 "avg": 140.46289447731755,
#                 "max": 255.0,
#                 "med": 142.0,
#                 "min": 1.5
#             }
#         },
#         "segment": {
#             "Animal": 0.0,
#             "Art": 0.0,
#             "Building": 0.20637020681270646,
#             "Fence": 0.2119193309763151,
#             "Field": 0.04286212337247294,
#             "Green": 0.06520388505736852,
#             "Ground": 0.03649951503828293,
#             "Human": 0.0006101131279360297,
#             "Light": 0.0,
#             "Other": 0.0048049202383240435,
#             "Path": 0.0,
#             "Rail": 0.0,
#             "Road": 0.03684368141814427,
#             "Sky": 0.270677918374462,
#             "Vehicle": 0.00010503779125638607,
#             "Wall": 0.03686602988436903,
#             "Water": 0.08723723790836235,
#             "Water_A": 0.0
#         },
#         "yolo": {
#             "person": 0.5,
#             "vehicle": 0.5
#         }
#     })
