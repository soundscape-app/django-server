import logging

from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter

from mirror.models import OrderMirror

logger = logging.getLogger(__name__)


@admin.register(OrderMirror)
class OrderMirrorAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(OrderMirrorAdmin, self).get_form(request, obj, **kwargs)
        return form

    def order_id(self, obj):
        _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/orders/{obj.id}'
        _link = f'<a href="{_url}" target="_blank">{obj.id}</a>'
        return format_html(_link)

    order_id.short_description = '주문 번호'

    def link_to_clayful_customer(self, obj):
        if obj.customer_id:
            _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/customers/{obj.customer_id}'
            _link = f'<a href="{_url}" target="_blank">{obj.address_customer_name}</a>'
            return format_html(_link)

        return f'{obj.address_customer_name}(비회원)'

    link_to_clayful_customer.short_description = '수취자'

    def product_name_with_links(self, obj):
        items = obj.json_dict.get('items', [])

        html_arr = []
        for item in items:
            product_name = item.get('product').get('name')
            brand_name = item.get('brand').get('name', '')
            product_id = item.get('product').get('_id')

            collections = item.get('collections')
            reketer_name = ''
            print(collections)

            if len(collections) > 0 and len(collections[0].get('path', [])) >= 2:
                reketer_name = f' - {collections[0].get("path")[1].get("name")}'

            _url = f'{settings.CLAYFUL_ADMIN_BASE_URL}/products/{product_id}'
            html_arr.append(f'<span><a href="{_url}" target="_blank">- {product_name}</a> [{brand_name}] {reketer_name}</span>')

        return format_html('<br>'.join(html_arr))

    product_name_with_links.short_description = '주문 상품'

    def payment_method_name(self, obj):
        return obj.payment_method_name

    payment_method_name.short_description = '결제 방법'

    def fullfillment_status(self, obj):
        return obj.fullfillment_status

    fullfillment_status.short_description = '배송 상태'

    def formatted_paid_amount(self, obj):
        return obj.formatted_paid_amount

    formatted_paid_amount.short_description = '결제 금액'

    list_display = [
        'order_id', 'product_name_with_links', 'link_to_clayful_customer',
        'status', 'formatted_paid_amount', 'paid_datetime', 'payment_method_name',
        'fullfillment_status',
    ]
    search_fields = ['id', 'product_names', 'address_customer_name']
    list_filter = (
        'status',
        ('paid_datetime', DateRangeFilter),
    )

    fields = list_display

    def get_queryset(self, request):
        qs = super(OrderMirrorAdmin, self).get_queryset(request)

        return qs.filter(paid_datetime__isnull=False).order_by('-paid_datetime')
