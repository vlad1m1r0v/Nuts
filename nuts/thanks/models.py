from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from core.blocks import ImageJumbotronBlock


class ThanksPage(Page):
    hero = StreamField(
        [
            ('image_jumbotron', ImageJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    content_panels = Page.content_panels + [
        FieldPanel('hero'),
    ]

    class Meta:
        verbose_name = "Thanks page"