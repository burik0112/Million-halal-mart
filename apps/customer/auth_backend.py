from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class PhoneAuthBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = User.objects.get(profile__phone_number=phone_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            raise ValidationError("Invalid phone number or password")
        return None
