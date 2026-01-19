from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class RegisterPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['custom_auth.TermsOfUsePage']
    max_count = 1

    class Meta:
        verbose_name = "Register page"


class TermsOfUsePage(Page):
    parent_page_types = ['custom_auth.RegisterPage']
    subpage_types = []
    max_count = 1

    template = "terms_of_use.html"

    description = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]

    class Meta:
        verbose_name = "Terms of use page"
