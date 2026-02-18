from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.views import View
from django.utils.translation import gettext as _

from profiles.forms import (
    LegalEntityContactInformationForm,
    IndividualContactInformationForm,
    BusinessAddressForm,
    IndividualAddressForm,
    ChangePasswordForm
)


class UpdateContactInformationView(View):
    def post(self, request):
        user = request.user
        profile = user.customer_profile
        is_business = hasattr(profile, 'business_profile')

        FormClass = LegalEntityContactInformationForm if is_business else IndividualContactInformationForm
        form = FormClass(request.POST, request.FILES, user=user)

        if form.is_valid():
            form.save()
            messages.success(request, _("Ваши контактные данные успешно обновлены."))
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            return redirect(request.META.get('HTTP_REFERER', '/'))


class UpdateAddressInformationView(View):
    def post(self, request):
        user = request.user
        profile = user.customer_profile
        is_business = hasattr(profile, 'business_profile')

        FormClass = BusinessAddressForm if is_business else IndividualAddressForm
        form = FormClass(request.POST, user=user)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, _("Адрес и реквизиты успешно обновлены."))
            except Exception as e:
                messages.error(request, _("Произошла ошибка при сохранении: %(error)s") % {'error': str(e)})

            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            return redirect(request.META.get('HTTP_REFERER', '/'))


class UpdatePasswordView(View):
    def post(self, request):
        form = ChangePasswordForm(request.POST, user=request.user)

        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data.get("new_password")
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, _("Ваш пароль успешно изменен."))
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            return redirect(request.META.get('HTTP_REFERER', '/'))