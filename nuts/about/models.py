from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image

from wagtailmedia.blocks import VideoChooserBlock

from core.blocks import VideoJumbotronBlock, ImageJumbotronBlock


class AboutPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    description = models.TextField(blank=True)

    hero = StreamField(
        [
            ("video_jumbotron", VideoJumbotronBlock()),
        ],
        blank=True,
        use_json_field=True,
        max_num=1
    )

    videos = StreamField([
        ('video', VideoChooserBlock())
    ], blank=True, use_json_field=True)

    owner_photo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    owner_cite = models.CharField(max_length=255, blank=True)
    owner_description = models.TextField(blank=True)
    write_us = models.URLField(blank=True)

    company_history_title = models.CharField(max_length=255, blank=True)
    company_history_description = models.TextField(blank=True)

    image_hero = StreamField(
        [
            ("image_jumbotron", ImageJumbotronBlock()),
        ],
        blank=True,
        use_json_field=True,
        max_num=1
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("hero"),
        FieldPanel("videos"),
        FieldPanel("owner_photo"),
        FieldPanel("owner_cite"),
        FieldPanel("owner_description"),
        FieldPanel("write_us"),
        FieldPanel("company_history_title"),
        FieldPanel("company_history_description"),
        FieldPanel("image_hero"),
    ]

    class Meta:
        verbose_name = "About page"
