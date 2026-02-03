import logging

from django.db import transaction
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import redirect

from auth.forms import IndividualRegistrationForm
from auth.models import RegisterPage

from locations.models import Address

from users.models import CustomerProfile

from home.models import HomePage

logger = logging.getLogger(__name__)


class IndividualRegistrationView(View):
    def post(self, request, *args, **kwargs):
        register_page = RegisterPage.objects.live().public().first()
        register_url = register_page.get_url(request)

        home_page = HomePage.objects.live().public().first()
        home_url = home_page.get_url(request)

        form = IndividualRegistrationForm(request.POST, request.FILES)

        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    logger.error(error)
                    messages.error(request, error)

            return redirect(register_url)

        try:
            with transaction.atomic():
                data = form.cleaned_data

                password = make_password(data['password'])

                user = User.objects.create_user(
                    username=data['full_name'],
                    email=data['email'],
                    password=password,
                    is_staff=False,
                    is_superuser=False,
                    is_active=True
                )

                contact_address = Address.objects.create(
                    region=data['region'],
                    city=data['city'],
                    street_address=data.get('address_line', None)
                )

                CustomerProfile.objects.create(
                    user=user,
                    contact_address=contact_address,
                    avatar=data.get('avatar'),
                    full_name=data['full_name'],
                    phone=data['phone'],
                    agreed_to_terms=data['agreed_to_terms'],
                    is_fop=data.get('is_fop', False)
                )

            messages.success(request, "Регистрация прошла успешно. Теперь вы можете войти.")
            return redirect(home_url)

        except Exception as e:
            messages.error(request, "Произошла внутренняя ошибка сервера. Попробуйте позже.")
            return redirect(register_url)