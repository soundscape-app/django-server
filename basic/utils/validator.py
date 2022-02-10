from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.core.exceptions import ValidationError

def is_valid_password(password):
    try: 
        password_validators = [
            UserAttributeSimilarityValidator(),
            MinimumLengthValidator(8),
            CommonPasswordValidator(),
            NumericPasswordValidator(),
        ]
        for validator in password_validators:
            validator.validate(password)
        return True, None
    except ValidationError as e:
        return False, str(e).replace('[', '').replace(']', '').replace("'", '')