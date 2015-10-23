from django.contrib.auth.models import User
from accounts.models import UserProfile


class Backend(object):

    def authenticate(self, phone=None, sms_code=None):
        if (phone and sms_code) is not None:
            try:
                user_profile = UserProfile.objects.get(phone=phone, sms_code=sms_code)
                user_profile.user.backend = 'django.contrib.auth.backends.ModelBackend'
                return user_profile.user
            except User.DoesNotExist:
                return None

    def get_user(self, phone):
        try:
            user_profile = UserProfile.objects.get(phone=phone)
            return user_profile.user
        except User.DoesNotExist:
            return None