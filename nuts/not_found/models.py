from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from wagtail.models import Page

from home.models import HomePage


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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context["home_page"] = HomePage.objects.live().public().first()

        return context


    content_panels = Page.content_panels + [
        FieldPanel("hero_text"),
        FieldPanel("background_image_photo"),
        FieldPanel("subtitle"),
        FieldPanel("button_text")
    ]