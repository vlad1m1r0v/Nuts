import logging

from django.db import transaction
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import redirect

from auth.forms import (
    IndividualRegistrationForm,
    BusinessRegistrationForm
)
from auth.models import RegisterPage

from locations.models import Address

from users.models import (
    CustomerProfile,
    BusinessProfile,
    FOPDetails,
    LegalEntityDetails
)

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


class BusinessRegistrationView(View):
    def post(self, request, *args, **kwargs):
        register_page = RegisterPage.objects.live().public().first()
        register_url = register_page.get_url(request) if register_page else '/'

        home_page = HomePage.objects.live().public().first()
        home_url = home_page.get_url(request) if home_page else '/'

        form = BusinessRegistrationForm(request.POST, request.FILES)

        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect(register_url)

        try:
            with transaction.atomic():
                data = form.cleaned_data
                b_type_raw = data['business_type']

                user = User.objects.create_user(
                    username=data['full_name'],
                    email=data['email'],
                    password=data['password'],
                    is_active=True
                )

                contact_address = Address.objects.create(
                    region=data['region'],
                    city=data['city'],
                    street_address=data.get('address_line', None)
                )

                customer = CustomerProfile.objects.create(
                    user=user,
                    contact_address=contact_address,
                    avatar=data.get('avatar'),
                    full_name=data['full_name'],
                    phone=data['phone'],
                    agreed_to_terms=data['agreed_to_terms'],
                    is_fop=(b_type_raw == 'fop')
                )

                b_type_map = {
                    'ur': BusinessProfile.BusinessType.LEGAL_ENTITY,
                    'fop': BusinessProfile.BusinessType.FOP
                }

                business_profile = BusinessProfile.objects.create(
                    customer=customer,
                    business_type=b_type_map[b_type_raw]
                )

                if b_type_raw == 'ur':
                    legal_addr = Address.objects.create(
                        region=data['legal_region'],
                        city=data['legal_city'],
                        street_address=data.get('legal_address_line', None),
                        postal_code=data.get('legal_index', None)
                    )
                    LegalEntityDetails.objects.create(
                        business=business_profile,
                        legal_address=legal_addr,
                        okpo_code=data['okpo']
                    )
                else:
                    activity_addr = Address.objects.create(
                        region=data['fop_region'],
                        city=data['fop_city'],
                        street_address=data.get('fop_address_line', None)
                    )
                    FOPDetails.objects.create(
                        business=business_profile,
                        activity_address=activity_addr,
                        edrpo_code=data['edrpo']
                    )

            messages.success(request, "Бизнес-аккаунт успешно зарегистрирован.")
            return redirect(home_url)

        except Exception as e:
            logger.error(e)
            messages.error(request, "Произошла внутренняя ошибка сервера. Попробуйте позже.")
            return redirect(register_url)
