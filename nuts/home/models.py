from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from core.blocks import VideoJumbotronBlock, ImageJumbotronBlock

class HomePage(Page):
    video_hero = StreamField(
        [
            ('video_jumbotron', VideoJumbotronBlock()),
        ],
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    products_title = models.CharField(
        max_length=100,
        blank=True,
    )

    products_subtitle = models.TextField(
        blank=True,
    )

    video_hero_2 = StreamField(
        [
            ('video_jumbotron', VideoJumbotronBlock()),
        ],
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    product_utility_title = models.CharField(
        max_length=100,
        blank=True,
    )

    product_utility_description = models.TextField(
        blank=True,
    )

    walnut_utility_description = models.TextField(
        blank=True,
    )

    hazelnut_utility_description = models.TextField(
        blank=True,
    )

    rosehip_utility_description = models.TextField(
        blank=True,
    )

    image_hero = StreamField(
        [
            ('image_jumbotron', ImageJumbotronBlock()),
        ],
        max_num=1,
        blank=True,
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('video_hero'),

        FieldPanel('products_title'),
        FieldPanel('products_subtitle'),

        FieldPanel('video_hero_2'),

        FieldPanel('product_utility_title'),
        FieldPanel('product_utility_description'),

        FieldPanel('walnut_utility_description'),
        FieldPanel('hazelnut_utility_description'),
        FieldPanel('rosehip_utility_description'),

        FieldPanel('image_hero'),
    ]

