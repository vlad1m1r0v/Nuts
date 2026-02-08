from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from wagtail.models import Page


class NotFoundPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    template = "404.html"

    hero_text = models.CharField(max_length=100, null=True, blank=True)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    background_image_photo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    button_text = models.CharField(max_length=100, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("hero_text"),
        FieldPanel("subtitle"),
        FieldPanel("button_text")
    ]