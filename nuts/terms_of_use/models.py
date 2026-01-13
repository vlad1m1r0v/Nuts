from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class TermsOfUsePage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    template = "terms_of_use.html"

    description = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]

    class Meta:
        verbose_name = "Terms of use page"