from django.contrib import messages
from django.shortcuts import redirect

from auth.models import LoginPage


class CustomerProfileRequiredMixin:
    def serve(self, request, *args, **kwargs):
        login_page = LoginPage.objects.live().public().first()
        login_url = login_page.get_url(request)

        if any([
            request.user.is_anonymous,
            request.user.is_staff,
            request.user.is_superuser,
            not hasattr(request.user, "customer_profile"),
        ]):
            messages.warning(request, "Для доступа к этой странице необходимо войти в аккаунт.")
            return redirect(login_url)

        return super().serve(request, *args, **kwargs)
