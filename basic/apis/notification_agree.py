from rest_framework.views import APIView
from rest_framework.response import Response

from backend.models import Customer


class NotificationAgreeAPI(APIView):
    def get(self, request):
        clayful_customer_id = request.GET.get("clayful_customer_id")

        customer = Customer.objects.get(clayful_customer_id=clayful_customer_id)

        return Response({
            'product_opening_notification_agreement': customer.product_opening_notification_agreement,
            'new_product_registration_notification_agreement': customer.new_product_registration_notification_agreement
            })

    def post(self, request, *args, **kwargs):
        clayful_customer_id = request.data.get('clayful_customer_id')
        product_opening_notification_agreement = request.data.get('product_opening_notification_agreement')
        new_product_registration_notification_agreement = request.data.get('new_product_registration_notification_agreement')

        customer = Customer.objects.get(clayful_customer_id=clayful_customer_id)
        customer.product_opening_notification_agreement = product_opening_notification_agreement
        customer.new_product_registration_notification_agreement = new_product_registration_notification_agreement
        customer.save()

        return Response({})
