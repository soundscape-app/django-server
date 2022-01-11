import logging
from datetime import datetime, timedelta

from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status

from basic.models.prediction import Prediction
from basic.models.media import VideoResult

class UploadViewSet(viewsets.ViewSet):
    http_method_names = ["post", "get"]

    @action(detail=False, methods=['POST'])
    def video(self, request):
        data = request.data
        
        video = data.get('video')
        revisitation = float(data.get('revisitation'))
        loudness = float(data.get('loudness'))
        
        if not video:
            return Response({"message": "Video is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        video_result = VideoResult.objects.create(
            video=video,
            revisitation=revisitation,
            loudness=loudness
        )
        video_result.status = 'uploaded'
        video_result.save()
        
        res = dict()
        res['video_id'] = video_result.video_id
        res['revisitation'] = revisitation
        res['loudness'] = loudness
        res['uploaded_at'] = video_result.created_datetime

        return Response(res, status=status.HTTP_200_OK)




    # @action(detail=False, methods=['GET'])
    # # @method_decorator(parse_header())
    # def issued(self, request, *args, **kwargs):
    #     """고객에게 발급된 Coupon 목록을 가져옵니다"""

    #     clayful_customer_id = None
    #     if request.customer:
    #         clayful_customer_id = request.customer.clayful_customer_id

    #     coupon_issue = CouponIssue.objects.filter(
    #         clayful_customer_id=clayful_customer_id,
    #     )
        
    #     queryset = CouponMirror.objects.filter(
    #         id__in=coupon_issue.values_list('clayful_coupon_id', flat=True),
    #         active=True,
    #         expires_at__gte=(datetime.now() - timedelta(days=7)),
    #     )

    #     results = []
    #     for coupon in queryset:
    #         data = coupon.json_dict
    #         data = coupon_serializer(
    #             coupon,
    #             clayful_customer_id=clayful_customer_id,
    #         )
    #         results.append(data)

