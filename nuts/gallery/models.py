from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from wagtailmedia.blocks import VideoChooserBlock

from core.blocks import VideoJumbotronBlock

from .blocks import GalleryImageWithTextBlock


class GalleryPage(Page):
    hero = StreamField(
        [
            ('video_jumbotron', VideoJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1
    )

    subtitle = models.CharField(
        max_length=255,
        blank=True,
    )

    content = StreamField(
        [
            ('video', VideoChooserBlock()),
            ('image_with_text', GalleryImageWithTextBlock()),
            ('video_jumbotron', VideoJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('hero'),
        FieldPanel('content'),
    ]


    class Meta:
        verbose_name = "Gallery page"