from django.urls import path

from auth.views import (
    IndividualRegistrationView,
    BusinessRegistrationView,
    CustomerLoginView,
    CustomerForgotPasswordView,
    CustomerResetPasswordView
)

app_name = 'custom_auth'

urlpatterns = [
    path(
        route="registration/individual/",
        view=IndividualRegistrationView.as_view(),
        name="individual-registration"
    ),
    path(
        route="registration/business/",
        view=BusinessRegistrationView.as_view(),
        name="business-registration"
    ),
    path(
        route="login/",
        view=CustomerLoginView.as_view(),
        name="login"
    ),
    path(
        route="forgot-password/",
        view=CustomerForgotPasswordView.as_view(),
        name="forgot-password"
    ),
    path(
        route="reset-password/",
        view=CustomerResetPasswordView.as_view(),
        name="reset-password"
    )
]
