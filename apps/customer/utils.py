import random
from .models import Profile


def generate_otp():
    return random.randint(1000, 9999)


def user_lang(language, user_id):
    user = Profile.objects.get(id=user_id)
    user.lang = language
    user.save()
