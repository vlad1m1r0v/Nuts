from django.db import transaction
from django.shortcuts import redirect
from django.contrib import messages
from django.views import View

from profiles.forms import (
    LegalEntityContactInformationForm,
    IndividualContactInformationForm,
    BusinessAddressForm,
    IndividualAddressForm
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
            messages.success(request, "Ваши контактные данные успешно обновлены.")
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
                messages.success(request, "Адрес и реквизиты успешно обновлены.")
            except Exception as e:
                messages.error(request, f"Произошла ошибка при сохранении: {str(e)}")

            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            return redirect(request.META.get('HTTP_REFERER', '/'))
