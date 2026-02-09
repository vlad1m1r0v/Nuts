from django.db import models
from wagtail.images.models import Image

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from core.blocks import VideoJumbotronBlock, ImageJumbotronBlock

from about.models import AboutPage

from news.models import NewsIndexPage, NewsDetailPage

class HomePage(Page):
    parent_page_types = []
    template = 'home.html'

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

    walnut_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    walnut_utility_description = models.TextField(
        blank=True,
    )

    hazelnut_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    hazelnut_utility_description = models.TextField(
        blank=True,
    )

    rosehip_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context["about_page"] = AboutPage.objects.live().public().first()
        context["news_page"] = NewsIndexPage.objects.live().first()
        context["news_list"] = NewsDetailPage.objects.live().order_by('-publication_date')[:3]

        return context

    content_panels = Page.content_panels + [
        FieldPanel('video_hero'),

        FieldPanel('products_title'),
        FieldPanel('products_subtitle'),

        FieldPanel('video_hero_2'),

        FieldPanel('product_utility_title'),
        FieldPanel('product_utility_description'),

        FieldPanel('walnut_image'),
        FieldPanel('walnut_utility_description'),

        FieldPanel('hazelnut_image'),
        FieldPanel('hazelnut_utility_description'),

        FieldPanel('rosehip_image'),
        FieldPanel('rosehip_utility_description'),

        FieldPanel('image_hero'),
    ]

