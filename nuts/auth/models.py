from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from auth.forms import IndividualRegistrationForm


class RegisterPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['custom_auth.TermsOfUsePage']
    max_count = 1

    template = "auth/register.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context["individual_registration_form"] = IndividualRegistrationForm()
        context["terms_page"] = TermsOfUsePage.objects.live().public().first()

        return context


    class Meta:
        verbose_name = "Register page"


class LoginPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    template = "auth/login.html"

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
