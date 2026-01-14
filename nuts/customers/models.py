from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel

from core.blocks import ImageJumbotronBlock

from .blocks import CustomerInfoBlock

class CustomersPage(Page):
    template = "customers.html"

    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    hero = StreamField(
        [
            ('image_jumbotron', ImageJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    description_column_1 = RichTextField(blank=True)
    description_column_2 = RichTextField(blank=True)

    supermarkets = StreamField(
        [
            ('customer_info_block', CustomerInfoBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    retail_stores = StreamField(
        [
            ('customer_info_block', CustomerInfoBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    horeca = StreamField(
        [
            ('customer_info_block', CustomerInfoBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    fitness_clubs = StreamField(
        [
            ('customer_info_block', CustomerInfoBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    confectionary_bakeries = StreamField(
        [
            ('customer_info_block', CustomerInfoBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    image_hero = StreamField(
        [
            ('image_jumbotron', ImageJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    content_panels = Page.content_panels + [
        FieldPanel('hero'),
        FieldPanel('description_column_1'),
        FieldPanel('description_column_2'),
        FieldPanel('supermarkets'),
        FieldPanel('retail_stores'),
        FieldPanel('horeca'),
        FieldPanel('fitness_clubs'),
        FieldPanel('confectionary_bakeries'),
        FieldPanel('image_hero'),
    ]
