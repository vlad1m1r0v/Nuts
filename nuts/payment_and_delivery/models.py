from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from core.blocks import VideoJumbotronBlock, ImageJumbotronBlock

from .blocks import PaymentAndDeliveryInfoSectionBlock


class PaymentAndDeliveryPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    image_hero = StreamField(
        [
            ('image_jumbotron', ImageJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    payment_info = StreamField(
        [
            ('info_section_block', PaymentAndDeliveryInfoSectionBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    delivery_info = StreamField(
        [
            ('info_section_block', PaymentAndDeliveryInfoSectionBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    return_info = StreamField(
        [
            ('info_section_block', PaymentAndDeliveryInfoSectionBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    video_hero = StreamField(
        [
            ('video_jumbotron', VideoJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    content_panels = Page.content_panels + [
        FieldPanel('image_hero'),
        FieldPanel('payment_info'),
        FieldPanel('delivery_info'),
        FieldPanel('return_info'),
        FieldPanel('video_hero')
    ]

    class Meta:
        verbose_name = "Payment and delivery page"
