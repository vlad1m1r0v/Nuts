from django.db import models

from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from .blocks import ProductImageWithTextBlock


@register_setting
class ProductCommonSettings(BaseSiteSetting):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    storage_conditions = models.TextField(blank=True, null=True)

    description_info = StreamField(
        [
            ('image_with_text', ProductImageWithTextBlock()),
        ],
        use_json_field=True,
        max_num=1,
        blank=True,
        null=True,
    )

    packaging_info = StreamField(
        [
            ('image_with_text', ProductImageWithTextBlock()),
        ],
        use_json_field=True,
        max_num=1,
        blank=True,
        null=True,
    )

    payment_info = StreamField(
        [
            ('image_with_text', ProductImageWithTextBlock()),
        ],
        use_json_field=True,
        max_num=1,
        blank=True,
        null=True,
    )

    delivery_info = StreamField(
        [
            ('image_with_text', ProductImageWithTextBlock()),
        ],
        use_json_field=True,
        max_num=1,
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel("storage_conditions"),
        FieldPanel("description_info"),
        FieldPanel("packaging_info"),
        FieldPanel("payment_info"),
        FieldPanel("delivery_info")
    ]

    class Meta:
        verbose_name = 'Product common settings'
