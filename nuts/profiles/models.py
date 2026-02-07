from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image

from auth.mixins import CustomerProfileRequiredMixin

from profiles.forms import (
    IndividualContactInformationForm,
    LegalEntityContactInformationForm
)

class ProfilePage(CustomerProfileRequiredMixin, Page):
    parent_page_types = ['home.HomePage']
    subpage_types = [
        'profiles.OrdersHistoryPage',
        'profiles.TransactionsHistoryPage',
        'profiles.ContactInformationPage',
        'profiles.AddressPage',
        'profiles.ChangePasswordPage'
    ]
    max_count = 1

    template = "profile/base.html"

    class Meta:
        verbose_name = "Profile page"


class OrdersHistoryPage(CustomerProfileRequiredMixin, Page):
    parent_page_types = ['profiles.ProfilePage']
    subpage_types = []
    max_count = 1

    template = "profile/orders_history.html"

    class Meta:
        verbose_name = "Orders history page"


class TransactionsHistoryPage(CustomerProfileRequiredMixin, Page):
    parent_page_types = ['profiles.ProfilePage']
    subpage_types = []
    max_count = 1

    template = "profile/transactions_history.html"

    class Meta:
        verbose_name = "Transactions history page"

class ContactInformationPage(CustomerProfileRequiredMixin, Page):
    parent_page_types = ['profiles.ProfilePage']
    subpage_types = []
    max_count = 1

    template = "profile/contact_information.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        user = request.user
        profile = user.customer_profile

        is_business = hasattr(profile, 'business_profile')

        initial_data = {
            'email': user.email,
            'phone': profile.phone,
            'full_name': profile.full_name,
        }

        if is_business:
            initial_data['company_name'] = profile.company_name
            form = LegalEntityContactInformationForm(initial=initial_data, user=user)
        else:
            form = IndividualContactInformationForm(initial=initial_data, user=user)

        context["form"] = form
        context["is_business"] = is_business
        return context



    class Meta:
        verbose_name = "Contact information page"


class ChangePasswordPage(CustomerProfileRequiredMixin, Page):
    parent_page_types = ['profiles.ProfilePage']
    subpage_types = []
    max_count = 1

    template = "profile/password.html"

    class Meta:
        verbose_name = "Change password page"


class AddressPage(CustomerProfileRequiredMixin, Page):
    parent_page_types = ['profiles.ProfilePage']
    subpage_types = []
    max_count = 1

    template = "profile/address.html"

    side_image_photo =  models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    side_image_title = models.CharField(max_length=100, null=True, blank=True)
    side_image_description = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("side_image_photo"),
        FieldPanel("side_image_title"),
        FieldPanel("side_image_description")
    ]

    class Meta:
        verbose_name = "Address page"

