import datetime
import logging
import xlwt

from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.utils.html import format_html
from django.contrib.admin.utils import flatten_fieldsets
from django.db.models import F, Subquery, Count, OuterRef

from mirror.models import (
    ProductMirror,
    BrandMirror,
    CollectionMirror,
    VendorMirror,
    ProductCategoryMap,
    ProductCollectionMap,
)
from partner.models import Partner
from backend.models import ProductHeartLog, ProductViewLog

from rangefilter.filters import DateRangeFilter
import csv
import json

logger = logging.getLogger(__name__)

not_included_to_csv = [
    'created_datetime',
    'updated_datetime',
    'id',
    # 'name',
    'summary',
    'description',
    'thumbnail',
    # 'available',
    # 'quantity',
    'num_variants',
    'price_type',
    # 'original_price',
    # 'sale_price',
    'is_new_product',
    # 'brand_id',
    # 'reketer_id',
    'open_date',
    'search_text',
    # 'json'  # for get category
]


class CategoryFilter(admin.SimpleListFilter):
    title = '카테고리'
    parameter_name = 'category'
    
    def lookups(self, request, model_admin):
        results = [('_', '(없음)')]
        category_list = ProductCategoryMap.objects.values_list('category', flat=True).distinct().order_by('-category')
        for _category in category_list:
            results.append((_category, _category))
        return results

    def queryset(self, request, queryset):
        if self.value() == '_':
            product_ids = ProductCategoryMap.objects.all().values_list('product_mirror_id', flat=True)
            return queryset.exclude(id__in=product_ids)
        else:
            product_ids = ProductCategoryMap.objects.filter(category=self.value()).values_list('product_mirror_id', flat=True)
            if self.value():
                return queryset.filter(id__in=product_ids)
            else:
                return queryset


class CollectionFilter(admin.SimpleListFilter):
    title = '컬렉션'
    parameter_name = 'collection_id'
    
    def lookups(self, request, model_admin):
        results = []
        collections = CollectionMirror.objects.order_by('collection_type', 'name')
        for _collection in collections:
            if _collection.collection_type == 'category': continue
            if not _collection.parent_id: continue
            results.append((_collection.id, f'{_collection.collection_type} - {_collection.name}'))
        return results

    def queryset(self, request, queryset):
        product_ids = ProductCollectionMap.objects.filter(collection_id=self.value()).values_list('product_mirror_id', flat=True)
        if self.value():
            return queryset.filter(id__in=product_ids)
        else:
            return queryset


class BrandFilter(admin.SimpleListFilter):
    title = '브랜드'
    parameter_name = 'brand_id'
    
    def lookups(self, request, model_admin):
        results = []
        brands = BrandMirror.objects.all().order_by('name')
        for _brand in brands:
            results.append((_brand.id, f'{_brand.name}'))
        return results

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(brand_id=self.value())
        else:
            return queryset


class VendorFilter(admin.SimpleListFilter):
    title = '입점사'
    parameter_name = 'vendor_id'

    def lookups(self, request, model_admin):
        results = [('_', '(없음)')]
        vendors = VendorMirror.objects.all().order_by('name')
        for _vendor in vendors:
            results.append((_vendor.id, f'{_vendor.name}'))
        return results

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == '_': 
                return queryset.filter(vendor_id=None)
            else: 
                return queryset.filter(vendor_id=self.value())
        else:
            return queryset


@admin.register(ProductMirror)
class ProductMirrorAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        return super(ProductMirrorAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(ProductMirrorAdmin, self).get_queryset(request)
        qs = qs.order_by('-created_datetime')
        qs = qs.annotate(
            price_delta=F('original_price') - F('sale_price'),
            count_heart=Subquery(
                ProductHeartLog.objects.filter(
                    clayful_product_id=OuterRef('id'), 
                    is_hearted=True,
                    updated_datetime__gte=datetime.datetime.now() - datetime.timedelta(days=30),
                ).values('clayful_product_id').annotate(count=Count('clayful_product_id')).values('count')[:1]
            ),
            count_view=Subquery(
                ProductViewLog.objects.filter(
                    clayful_product_id=OuterRef('id'),
                    updated_datetime__gte=datetime.datetime.now() - datetime.timedelta(days=7),
                ).values('clayful_product_id').annotate(count=Count('clayful_product_id')).values('count')[:1]
            ),
        )
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
        _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/products/{obj.id}'
        _link = f'<a href="{_url}" target="_blank">{obj.id}</a>'
        return format_html(_link)
    
    def product_thumbnail(self, obj):
        _html = f'<img src="{obj.thumbnail}" width="60" height="60">'
        return format_html(_html)

    def product_name(self, obj):
        _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/products/{obj.id}'
        _link = f'<a href="{_url}" target="_blank"><p style="width:200px">{obj.name}</p></a>'
        return format_html(_link)
    
    def original_price_str(self, obj):
        return f'{obj.original_price:,}'

    def sale_price_str(self, obj):
        return f'{obj.sale_price:,}'

    def price_delta(self, obj):
        discount = obj.original_price - obj.sale_price
        percent = discount / obj.original_price * 100 if obj.original_price > 0 else 0
        return f'-{discount:,} ({percent:.1f}%)'

    # def category(self, obj):
    #     return obj.category

    def category_name(self, obj):
        category_list = ProductCategoryMap.objects.filter(product_mirror_id=obj.id).values_list('category', flat=True)
        if not category_list: return None
        _url = f'{self.path}'
        _links = []
        for category in category_list:
            _links.append(
                f'<li><a href="{_url}?category={category}">'
                f'<p style="width: 90px; line-height: normal; margin: 0px;">{category}</p></a></li>'
            )
        if not _links: return None
        return format_html('<ul style="font-size:0">'+''.join(_links)+'</ul>')
        # return format_html(''.join(_links))
        # category_list = [f'<li><p style="width: 100px; line-height: normal; margin: 0px;">{c}</p>' for c in category_list]
        # return format_html(''.join(category_list))

    def collection_id(self, obj):
        return obj.collection_id
    
    def collection_name(self, obj):
        collection_ids = ProductCollectionMap.objects.filter(product_mirror_id=obj.id).values_list('collection_id', flat=True)
        if not collection_ids: return None
        collections = CollectionMirror.objects.filter(
            id__in=collection_ids
        )
        _url = f'{self.path}'
        _links = []
        for _collection in collections:
            if _collection.collection_type == 'event':
                _links.append(
                    f'<li><a href="{_url}?collection_id={_collection.id}">'
                    f'<p style="width: 90px; line-height: normal; margin: 0px;">{_collection.name}</p></a></li>'
                )
        if not _links: return None
        return format_html('<ul style="font-size:0">'+''.join(_links)+'</ul>')

    def vendor_name(self, obj):
        vendor = VendorMirror.objects.filter(
            id=obj.vendor_id
        ).values('name').first()
        if not vendor: return None
        _url = f'{self.path}'
        _link = f'{vendor.get("name")} (<a href="{_url}?vendor_id={obj.vendor_id}">{obj.vendor_id}</a>)'
        return format_html(_link)

    def reketer_name(self, obj):
        collection = CollectionMirror.objects.filter(
            id=obj.reketer_id
        ).values('name').first()
        if not collection: return None
        _url = f'{self.path}'
        _link = f'{collection.get("name")} (<a href="{_url}?reketer_id={obj.reketer_id}">{obj.reketer_id}</a>)'
        return format_html(_link)

    def brand_name(self, obj):
        brand = BrandMirror.objects.filter(
            id=obj.brand_id
        ).values('name').first()
        if not brand: return None
        _url = f'{self.path}'
        _link = f'{brand.get("name")} (<a href="{_url}?brand_id={obj.brand_id}">{obj.brand_id}</a>)'
        return format_html(_link)
    
    def count_heart(self, obj):
        cnt = ProductHeartLog.objects.filter(
            clayful_product_id=obj.id,
            is_hearted=True,
        ).count()
        return cnt

    def count_view(self, obj):
        cnt = ProductViewLog.objects.filter(
            clayful_product_id=obj.id,
            created_datetime__gte=F('created_datetime') - datetime.timedelta(days=7),
        ).count()
        return cnt

    clayful_link.short_description = '클레이풀 상품 ID'
    clayful_link.admin_order_field = 'id'
    
    product_thumbnail.short_description = '썸네일'
    
    product_name.short_description = '상품명'
    product_name.admin_order_field = 'name'
    
    original_price_str.short_description = '정가'
    original_price_str.admin_order_field = 'original_price'
    
    sale_price_str.short_description = '할인가'
    sale_price_str.admin_order_field = 'sale_price'

    price_delta.short_description = '할인 정도'
    price_delta.admin_order_field = '-price_delta'

    category_name.short_description = '카테고리'
    # category_name.admin_order_field = 'category'
    
    collection_name.short_description = '컬렉션'
    # collection_name.admin_order_field = 'collection_id'

    vendor_name.short_description = '입점사'
    vendor_name.admin_order_field = 'vendor_id'
    
    reketer_name.short_description = '리켓터'
    reketer_name.admin_order_field = 'reketer_id'
    
    brand_name.short_description = '브랜드'
    brand_name.admin_order_field = 'brand_id'
    
    count_heart.short_description = '한달간 좋아요 수'
    count_heart.admin_order_field = '-count_heart'

    count_view.short_description = '일주일간 조회 수'
    count_view.admin_order_field = '-count_view'

    list_per_page = 50
    
    list_display = [
        'clayful_link', 'product_thumbnail', 'product_name', 
        'available', 'quantity', 'num_variants',
        'original_price_str', 'sale_price_str', 'price_delta',
        'count_heart', 'count_view',
        'category_name',
        'collection_name',
        'vendor_name',
        'reketer_name',
        'brand_name',
        'created_datetime', 'updated_datetime',
    ]

    list_filter = [
        ('created_datetime', DateRangeFilter),
        ('updated_datetime', DateRangeFilter),
        CategoryFilter,
        VendorFilter,
        CollectionFilter,
        BrandFilter,
    ]

    search_fields = [
        'id',
        'name',
        'vendor_id',
        'reketer_id',
        'brand_id',
    ]

    # download csv file from django admin page
    def export_as_csv(self, request, queryset):
        # from collection mirror table, get reketer names
        reketer_names = list(CollectionMirror.objects.all().values('name').values_list('id', 'name'))
        reketer_ID_to_reketer_name = {}
        brand_ID_to_brand_name = {}
        for reketer in reketer_names:
            reketer_ID_to_reketer_name[reketer[0]] = reketer[1]
        for brand in list(BrandMirror.objects.all().values('id', 'name')):
            brand_ID_to_brand_name[brand['id']] = brand['name']

        meta = self.model._meta
        field_names = [field.name for field in meta.fields if field.name not in not_included_to_csv]
        reketer_id_index = field_names.index('reketer_id')
        brand_id_index = field_names.index('brand_id')
        available_index = field_names.index('available')
        json_index = field_names.index('json')

        response = HttpResponse(content_type='text/csv', charset='utf-8')
        response['Content-Disposition'] = f'attachment; filename={format(meta)}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for idx, obj in enumerate(queryset):
            row = [getattr(obj, field) for field in field_names]
            if row[available_index]:
                try:
                    row[reketer_id_index] = reketer_ID_to_reketer_name[row[reketer_id_index]]
                    row[brand_id_index] = brand_ID_to_brand_name[row[brand_id_index]]
                    try:    row[json_index] = json.loads(row[json_index])['meta']['category']
                    except: row[json_index] = []
                    writer.writerow(row)
                except Exception as e:
                    print(e)
                    print(row)

        return response

    export_as_csv.short_description = "CSV로 export하기"
    
    # Download excel file from django admin page
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'example.xls'
        wb = xlwt.Workbook(encoding='ansi')  # encoding은 ansi로 해준다.
        ws = wb.add_sheet('Product Mirror')  # 시트 추가

        row_num = 0
        col_names = ['No.', '클레이풀 상품 ID', '상품명', '상품 수량', '품목 개수', '정가', '할인가', '입점사', '리켓터', '브랜드']

        # 열이름을 첫번째 행에 추가 시켜준다.
        for idx, col_name in enumerate(col_names):
            ws.write(row_num, idx, col_name)

        rows = queryset.all().values_list('id', 'name', 'quantity', 'num_variants', 'original_price', 'sale_price', 'vendor_id', 'reketer_id', 'brand_id')

        for row in rows:
            row_num += 1
            ws.write(row_num, 0, row_num)
            for col_num, attr in enumerate(row):
                if col_names[col_num+1] == '입점사':
                    vendor = VendorMirror.objects.filter(id=attr).first()
                    name = vendor.name if vendor else '-'
                    attr = f'{name} ({attr})'
                elif col_names[col_num+1] == '리켓터':
                    reketer = CollectionMirror.objects.filter(id=attr).first()
                    name = reketer.name if reketer else '-'
                    attr = f'{name} ({attr})'
                elif col_names[col_num+1] == '브랜드':
                    brand = BrandMirror.objects.filter(id=attr).first()
                    name = brand.name if brand else '-'
                    attr = f'{name} ({attr})'
                ws.write(row_num, col_num+1, attr)

        wb.save(response)
        return response

    export_as_excel.short_description = "XLS로 export하기"

    actions = [
        export_as_csv,
        export_as_excel,
    ]
