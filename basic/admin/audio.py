import logging

from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.utils.html import format_html
from django.contrib.admin.utils import flatten_fieldsets
from django.db.models import F, Subquery, OuterRef, Count
from django.utils.safestring import mark_safe

import time

# from mirror.models import (
#     ProductMirror,
#     Audio,
#     CollectionMirror,
# )
# from partner.models import Partner
# from backend.models import BrandHeartLog

# from rangefilter.filters import DateRangeFilter
# import csv
# import json

from basic.models import Audio, VideoResult

logger = logging.getLogger(__name__)


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        return super(AudioAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(AudioAdmin, self).get_queryset(request)
        return qs

    def fieldname_download(self, obj):
        return mark_safe(f'<a href="/media/{obj.wav_file}" download>download</a>')

    fieldname_download.short_description = 'Download'
    
    def duration_formatted(self, obj):
        if obj.duration is None: 
            return None
        return time.strftime('%H:%M:%S', time.gmtime(obj.duration))

    duration_formatted.short_description = 'duration'

    # def get_readonly_fields(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return self.readonly_fields

    #     if self.declared_fieldsets:
    #         return flatten_fieldsets(self.declared_fieldsets)
    #     else:
    #         return list(set(
    #             [field.name for field in self.opts.local_fields] +
    #             [field.name for field in self.opts.local_many_to_many]
    #         ))

    # def clayful_link(self, obj):
    #     _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/brands/{obj.id}'
    #     _link = f'<a href="{_url}" target="_blank">{obj.id}</a>'
    #     return format_html(_link)

    # def brand_name(self, obj):
    #     _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/brands/{obj.id}'
    #     _link = f'<a href="{_url}" target="_blank">{obj.name}</a>'
    #     return format_html(_link)
    
    # def num_products(self, obj):
    #     cnt = ProductMirror.objects.filter(brand_id=obj.id, available=True).count()
    #     return cnt
    
    # def num_total_products(self, obj):
    #     total = ProductMirror.objects.filter(brand_id=obj.id).count()
    #     return total

    # def count_heart(self, obj):
    #     cnt = BrandHeartLog.objects.filter(
    #         clayful_brand_id=obj.id,
    #         is_hearted=True,
    #     ).count()
    #     return cnt
    
    # def list_link(self, obj):
    #     clayful_url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/products?brand={obj.id}'
    #     django_url = f'{self.path.replace("Audio","productmirror")}?brand_id={obj.id}'
    #     _link = f'<a href="{clayful_url}" target="_blank">Clayful</a> / <a href="{django_url}" target="_blank">Django</a>'
    #     return format_html(_link)
    
    # def keywords(self, obj):
    #     json_dict = obj.json_dict
    #     result = ['-']
    #     if json_dict is not None and json_dict.get('meta'):
    #         result = json_dict.get('meta').get('aliases')
    #     return result
    
    # clayful_link.short_description = '클레이풀 브랜드 ID'
    # clayful_link.admin_order_field = 'id'
    
    # brand_name.short_description = '브랜드명'
    # brand_name.admin_order_field = 'name'

    # num_products.short_description = '판매 가능 상품수'
    # num_total_products.short_description = '전체 상품수'
    
    # count_heart.short_description = '좋아요 수'
    # count_heart.admin_order_field = '-count_heart'
    
    # list_link.short_description = '상품 목록'
    # keywords.short_description = '검색 키워드'
    
    # list_per_page = 20
    
    list_display = [
        'audio_id', 'wav_file', 'fieldname_download', 'title', 'duration_formatted', 'created_datetime', 'updated_datetime',
    ]

    # list_filter = [
    #     ('created_datetime', DateRangeFilter),
    # ]

    # search_fields = [
    #     'id', 'name', 'name_ko', 'search_text',
    # ]
