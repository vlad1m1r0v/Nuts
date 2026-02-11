from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock

from core.blocks import ImageJumbotronBlock

from shop.forms import ProductFilterForm

class ShopPage(Page):
    template = "shop.html"

    parent_page_types = ['home.HomePage']
    subpage_types = ['products.ProductPage']
    max_count = 1

    hero = StreamField(
        [
            ('image_jumbotron', ImageJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    nut_title = models.CharField(max_length=100, blank=True)
    nut_description = models.TextField(blank=True)

    gallery = StreamField(
        [
            ('image', ImageChooserBlock()),
        ],
        use_json_field=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('hero'),
        FieldPanel('nut_title'),
        FieldPanel('nut_description'),
        FieldPanel('gallery')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context["filter_form"] = ProductFilterForm()

        return context

    class Meta:
        verbose_name = "Shop page"