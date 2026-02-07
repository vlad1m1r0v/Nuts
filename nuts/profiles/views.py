from django.shortcuts import redirect
from django.contrib import messages
from django.views import View

from profiles.forms import (
    LegalEntityContactInformationForm,
    IndividualContactInformationForm
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