from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class TermsOfUsePage(Page):
    description = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]

    class Meta:
        verbose_name = "Terms of use page"