import logging

from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.utils.html import format_html
from django.contrib.admin.utils import flatten_fieldsets
from django.db.models import F

from mirror.models import (
    ProductMirror,
    BrandMirror,
    CollectionMirror,
    ProductCollectionMap,
)
from partner.models import Partner

from rangefilter.filters import DateRangeFilter
import csv
import json

logger = logging.getLogger(__name__)

CATEGORY_COLLECTION = "RVRSHEE9TP2C"


@admin.register(CollectionMirror)
class CollectionMirrorAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        return super(CollectionMirrorAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(CollectionMirrorAdmin, self).get_queryset(request)
        qs = qs.filter(parent_id__isnull=False)
        qs = qs.order_by('collection_type', 'parent_id', '-created_datetime')
        
        self.path = request.path
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

    def clayful_link(self, obj):
        _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/collections/{obj.id}'
        _link = f'<a href="{_url}" target="_blank">{obj.id}</a>'
        return format_html(_link)

    def collection_name(self, obj):
        _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/collections/{obj.id}'
        _link = f'<a href="{_url}" target="_blank">{obj.name}</a>'
        return format_html(_link)
    
    def parent_name(self, obj):
        parenet = CollectionMirror.objects.filter(id=obj.parent_id).first()
        if not parenet: return None
        _url = f'{self.path}'
        _link = f'{parenet.name} (<a href="{_url}?parent_id={obj.parent_id}">{obj.parent_id}</a>)'
        return format_html(_link)

    def num_products(self, obj):
        objects = ProductCollectionMap.objects.filter(collection_id=obj.id)
        cnt = objects.select_related('product_mirror').filter(product_mirror__available=True).count()
        return cnt

    def num_total_products(self, obj):
        total = ProductCollectionMap.objects.filter(collection_id=obj.id).count()
        return total

    def list_link(self, obj):
        clayful_url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/products?collection={obj.id}'
        django_url = f'{self.path.replace("collectionmirror","productmirror")}?collection_id={obj.id}'
        _link = f'<a href="{clayful_url}" target="_blank">Clayful</a> / <a href="{django_url}" target="_blank">Django</a>'
        return format_html(_link)

    clayful_link.short_description = '클레이풀 컬렉션 ID'
    clayful_link.admin_order_field = 'id'
    
    collection_name.short_description = '컬렉션명'
    collection_name.admin_order_field = 'name'
    
    parent_name.short_description = '상위 컬렉션'
    parent_name.admin_order_field = 'parent_id'
    
    num_products.short_description = '판매 가능 상품수'
    num_total_products.short_description = '전체 상품수'
    list_link.short_description = '상품 목록'
    
    list_per_page = 20
    
    list_display = [
        'clayful_link', 'collection_type', 'collection_name', 'parent_name',
        'visible', 'num_products', 'num_total_products', 'list_link',
        'open_date', 'created_datetime',
    ]

    list_filter = [
        'collection_type',
        ('created_datetime', DateRangeFilter),
    ]

    search_fields = [
        'id', 'name',
    ]
