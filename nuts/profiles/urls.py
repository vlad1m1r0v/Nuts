from django.urls import path

from profiles.views import (
    UpdateContactInformationView,
    UpdateAddressInformationView
)

app_name = 'profiles'

urlpatterns = [
    path(
        route="contact-information/",
        view=UpdateContactInformationView.as_view(),
        name="contact-information"
    ),
    path(
        route="address-information/",
        view=UpdateAddressInformationView.as_view(),
        name="address-information"
    )
]
