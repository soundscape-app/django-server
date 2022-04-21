import datetime
import logging

from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.utils.html import format_html
from django.contrib.admin.utils import flatten_fieldsets
from django.db.models import F, Subquery, Count, OuterRef

from mirror.models import CustomerMirror
from partner.models import Partner
from backend.models import Customer

from rangefilter.filters import DateRangeFilter
import csv
import json

logger = logging.getLogger(__name__)


class SocialLoginFilter(admin.SimpleListFilter):
    title = '소셜 로그인'
    parameter_name = 'social_login_vendor'

    def lookups(self, request, model_admin):
        results = [('none', '(없음)'), ('apple', 'Apple'), ('naver', 'Naver'), ('kakao', 'Kakao')]
        return results

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'none': 
                return queryset.filter(
                    social_login_vendor__isnull=True,
                    is_apple_login=False,
                )
            elif self.value() == 'apple':
                return queryset.filter(
                    social_login_vendor__isnull=True,
                    is_apple_login=True,
                )
            else: 
                return queryset.filter(social_login_vendor=self.value())
        else:
            return queryset


@admin.register(CustomerMirror)
class CustomerMirrorAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        return super(CustomerMirrorAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(CustomerMirrorAdmin, self).get_queryset(request)
        qs = qs.order_by('-created_datetime')
        return qs

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields

        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

    def is_active(self, obj):
        try:
            idx = Customer.objects.get(clayful_customer_id=obj.id).is_active
            _html = f'<img src="/static/admin/img/icon-{["no","yes"][int(idx)]}.svg" alt="{str(idx)}">'
            return format_html(_html)
        except:
            return '-'
    
    def admin_push(self, obj):
        try:
            idx = Customer.objects.get(clayful_customer_id=obj.id).expo_push_token is not None
            _html = f'<img src="/static/admin/img/icon-{["no","yes"][int(idx)]}.svg" alt="{str(idx)}">'
            return format_html(_html)
        except:
            return '-'
    
    def clayful_link(self, obj):
        _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/customers/{obj.id}'
        _link = f'<a href="{_url}" target="_blank">{obj.id}</a>'
        return format_html(_link)

    def customer_name(self, obj):
        _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/customers/{obj.id}'
        _link = f'<a href="{_url}" target="_blank">{obj.name}</a>'
        return format_html(_link)
    
    def social_login(self, obj):
        if obj.social_login_vendor:
            return obj.social_login_vendor
        else:
            return 'apple' if obj.is_apple_login else '-'

    is_active.short_description = '활성화 상태'
    
    admin_push.short_description = '푸시 수신 가능 여부'

    clayful_link.short_description = '클레이풀 고객 ID'
    clayful_link.admin_order_field = 'id'

    customer_name.short_description = '고객명'
    customer_name.admin_order_field = 'name'
    
    social_login.short_description = '소셜 로그인'
    social_login.admin_order_field = 'social_login_vendor'
    
    list_per_page = 30
    
    list_display = [
        'clayful_link', 'customer_name', 'alias',
        'email', 'mobile', 'social_login',
        'is_active', 'admin_push',
        'created_datetime', 'updated_datetime',
    ]

    list_filter = [
        ('created_datetime', DateRangeFilter),
        ('updated_datetime', DateRangeFilter),
        SocialLoginFilter,
    ]

    search_fields = [
        'id', 'name', 'email', 'mobile', 'alias',
    ]
