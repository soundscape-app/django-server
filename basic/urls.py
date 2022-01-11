from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

from rest_framework import routers

# from basic.apis.notification_agree import Notifications
# from backend.views import front
# from backend.apis.product_qna import ProductQNAAPI
# from backend.apis.login import AppleLoginAPI
# from backend.apis.seller import SellerViewSet
# from backend.apis.product import ProductViewSet
# from backend.apis.app_config import AppConfigAPI
# from backend.apis.draw_event import DrawEventViewSet
# from backend.apis.search import SearchViewSet
# from backend.apis.notification_agree import NotificationAgreeAPI

from basic.apis.upload import UploadViewSet
from basic.apis.process import ProcessViewSet

# from backend.apis.auth import AuthLoginAPI

router = routers.SimpleRouter(trailing_slash=False)
router.register('upload', UploadViewSet, basename='upload')
router.register('process', ProcessViewSet, basename='process')

# router.register('api/products', ProductViewSet, basename='product')
# router.register('api/draw_events', DrawEventViewSet, basename='draw_event')
# router.register('api/search', SearchViewSet, basename='search')

urlpatterns = [
    path('auth/', obtain_auth_token),
] + router.urls

# urlpatterns = [
    # path('image', front.view_ping, name='image'),
    # path('ping', front.view_ping, name='ping'),
    # path('terms', front.view_terms, name='terms'),
    # path('login', front.view_login, name='login'),
    # path('home', front.view_home, name='home-deeplink'),
    # path('apple-app-site-association', front.view_apple_app_site_association, name='apple-app-site-association'),
    # path('assetlinks.json', front.view_assetlinks, name='assetlinks'),
    # path('search_address', front.view_search_address, name='search_address'),
    # path('payment', front.view_payment, name='payment'),
    # path('payment_result', front.view_payment_result, name='payment_result'),
    # path('p/<product_id>', front.view_product_dynamic_link, name='product_dynamic_link'),
    # path('r/<reketer_id>', front.view_reketer_dynamic_link, name='reketer_dynamic_link'),
    # path('api/auth/login/', AuthLoginAPI.as_view()),
    # path('api/product/qna/', ProductQNAAPI.as_view()),
    # path('api/apple_login/', AppleLoginAPI.as_view()),
    # path('api/app_config/', AppConfigAPI.as_view(), name='app_config_api'),
    # path('api/notification_agree/', NotificationAgreeAPI.as_view()),
# ] + router.urls
