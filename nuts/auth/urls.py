from django.urls import path

from auth.views import (
    IndividualRegistrationView,
    BusinessRegistrationView
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
    )
]
