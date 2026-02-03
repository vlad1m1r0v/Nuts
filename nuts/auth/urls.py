from django.urls import path

from auth.views import IndividualRegistrationView

app_name = 'custom_auth'

urlpatterns = [
    path(
        route="registration/individual/",
        view=IndividualRegistrationView.as_view(),
        name="individual-registration"
    ),
]
