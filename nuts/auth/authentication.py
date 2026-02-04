from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class CustomerAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get('email')

        if email is None:
            return None

        try:
            user = User.objects.get(
                email=email,
                is_active=True,
                is_staff=False,
                is_superuser=False
            )

            if not hasattr(user, 'customer_profile'):
                return None

            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        except User.DoesNotExist:
            return None
        except Exception:
            return None

        return None
