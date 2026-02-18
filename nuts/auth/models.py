from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from auth.forms import (
    IndividualRegistrationForm,
    BusinessRegistrationForm,
    CustomerLoginForm,
    CustomerForgotPasswordForm,
    CustomerResetPasswordForm
)
from auth.tokens import account_activation_token


class RegisterPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['custom_auth.TermsOfUsePage']
    max_count = 1

    template = "auth/register.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context["individual_registration_form"] = IndividualRegistrationForm()
        context["business_registration_form"] = BusinessRegistrationForm()
        context["terms_page"] = TermsOfUsePage.objects.live().public().first()

        return context

    class Meta:
        verbose_name = "Register page"


class LoginPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    template = "auth/login.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context["customer_login_form"] = CustomerLoginForm()
        context["forgot_page"] = ForgotPasswordPage.objects.live().public().first()
        context["registration_page"] = RegisterPage.objects.live().public().first()

        return context

    class Meta:
        verbose_name = "Login page"


class TermsOfUsePage(Page):
    parent_page_types = ['custom_auth.RegisterPage']
    subpage_types = []
    max_count = 1

    template = "auth/terms_of_use.html"

    description = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]

    class Meta:
        verbose_name = "Terms of use page"


class ForgotPasswordPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    template = "auth/forgot_password.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context["forgot_password_form"] = CustomerForgotPasswordForm()

        return context

    class Meta:
        verbose_name = "Forgot password page"


class RecoverPasswordPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    template = "auth/recover_password.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context["reset_password_form"] = CustomerResetPasswordForm()

        return context

    def serve(self, request, *args, **kwargs):
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')

        forgot_page = ForgotPasswordPage.objects.live().public().first()
        forgot_url = forgot_page.get_url(request)

        if not uidb64 or not token:
            messages.error(request, _("Предоставленный токен доступа не валидный."))
            return redirect(forgot_url)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if not account_activation_token.check_token(user, token):
                messages.error(request, _("Предоставленный токен доступа не валидный."))
                return redirect(forgot_url)

            context = self.get_context(request)
            context["email"] = user.email

            return render(request, self.template, context)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, _("Предоставленный токен доступа не валидный."))
            return redirect(forgot_url)

    class Meta:
        verbose_name = "Recover password page"