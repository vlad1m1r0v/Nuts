import logging

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db import transaction
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect

from auth.forms import (
    IndividualRegistrationForm,
    BusinessRegistrationForm,
    CustomerLoginForm,
    CustomerForgotPasswordForm
)
from auth.models import (
    RegisterPage,
    LoginPage,
    ForgotPasswordPage,
    RecoverPasswordPage,
    CustomerResetPasswordForm
)
from auth.tokens import account_activation_token

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

                user = User.objects.create_user(
                    username=data['full_name'],
                    email=data['email'],
                    password=data['password'],
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

            login(request, user, backend="auth.authentication.CustomerAuthBackend")

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

            login(request, user, backend="auth.authentication.CustomerAuthBackend")

            messages.success(request, "Бизнес-аккаунт успешно зарегистрирован.")
            return redirect(home_url)

        except Exception as e:
            logger.error(e)
            messages.error(request, "Произошла внутренняя ошибка сервера. Попробуйте позже.")
            return redirect(register_url)


class CustomerLoginView(View):
    def post(self, request, *args, **kwargs):
        login_page = LoginPage.objects.live().public().first()
        login_url = login_page.get_url(request)

        home_page = HomePage.objects.live().public().first()
        home_url = home_page.get_url(request)

        form = CustomerLoginForm(request.POST)

        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect(login_url)

        data = form.cleaned_data

        user = authenticate(
            request,
            username=data['email'],
            password=data['password']
        )

        if user is not None:
            login(request, user, backend="auth.authentication.CustomerAuthBackend")
            messages.success(request, f"Вход выполнен успешно.")
            return redirect(home_url)
        else:
            messages.error(request, "Неверный E-Mail или пароль.")
            return redirect(login_url)


class CustomerForgotPasswordView(View):
    def post(self, request, *args, **kwargs):
        forgot_password_page = ForgotPasswordPage.objects.live().public().first()
        forgot_url = forgot_password_page.get_url(request)

        recover_password_page = RecoverPasswordPage.objects.live().public().first()
        recover_password_url = recover_password_page.get_url(request)

        form = CustomerForgotPasswordForm(request.POST)

        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect(forgot_url)

        data = form.cleaned_data

        user = User.objects.get(email=data['email'])

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        domain = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'
        reset_link = f"{protocol}://{domain}{recover_password_url}?uid={uid}&token={token}"

        message = EmailMessage(
            to=[data["email"]],
            subject="Восстановление пароля",
            body=render_to_string(
                template_name="auth/recover_password_email_message.html",
                context={"reset_link": reset_link}
            )
        )

        message.content_subtype = 'html'
        message.send(fail_silently=False)

        messages.success(request, "Вам на почту отправлена ссылка на сброс пароля.")

        return redirect(forgot_url)


class CustomerResetPasswordView(View):
    def post(self, request, *args, **kwargs):
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')

        login_page = LoginPage.objects.live().public().first()
        login_url = login_page.get_url(request)
        referer_url = request.META.get('HTTP_REFERER')

        form = CustomerResetPasswordForm(request.POST)

        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            return redirect(referer_url)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if account_activation_token.check_token(user, token):
                user.set_password(form.cleaned_data['password'])
                user.save()

                messages.success(request, "Ваш пароль был успешно изменен. Теперь вы можете войти.")
                return redirect(login_url)
            else:
                messages.error(request, "Срок действия ссылки истек или она неверна.")
                return redirect(request.META.get('HTTP_REFERER'))

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Произошла ошибка при идентификации пользователя.")
            return redirect(referer_url)


class CustomerLogoutView(View):
    def post(self, request, *args, **kwargs):
        login_page = LoginPage.objects.live().public().first()
        login_url = login_page.get_url(request)

        logout(request)
        messages.success(request, "Вы успешно вышли из своего аккаунта.")

        return redirect(login_url)