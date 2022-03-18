import logging

# from backend.utils import auth
# from backend.models import Customer
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


def parse_header():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            access_token = request.META.get('HTTP_AUTHORIZATION')
            device_info = request.META.get('HTTP_X_DIVICE_INFO')
            
            print('access_token:', access_token)
            print('device_info:', device_info)
            
            request.user = None
            if access_token:
                # data = auth.decode_jwt(access_token)
                # user_id = data['iternal_user_id']
                # customer = Customer.objects.get(id=user_id)
                access_token = access_token.replace('Token ', '')
                token_obj = Token.objects.filter(key=access_token).first()
                if token_obj:
                    request.user = token_obj.user
                    print('request.user:', request.user)

            if device_info:
                device_info = device_info.split(';')
                if len(device_info) >= 5:
                    """
                    Format: "app_version; platform_os; os_version; device_model; install_identifier;"
                    Example: "1.0.27; ios; 14.2; iPhone 11 Pro; 08y0asgwo3j4-19H524;"
                    """
                    request.app_version = device_info[0].strip()
                    request.os = device_info[1].strip()
                    request.os_version = device_info[2].strip()
                    request.device_model = device_info[3].strip()
                    request.install_identifier = device_info[4].strip()

            return func(request, *args, **kwargs)

        return wrapper

    return decorator

