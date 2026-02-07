from django.urls import path

from profiles.views import (
    UpdateContactInformationView
)

app_name = 'profiles'

urlpatterns = [
    path(
        route="contact-information/",
        view=UpdateContactInformationView.as_view(),
        name="contact-information"
    ),
]