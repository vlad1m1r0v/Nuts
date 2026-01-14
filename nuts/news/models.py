from django.db import models

from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from wagtailmedia.blocks import VideoChooserBlock

from core.blocks import VideoJumbotronBlock


class NewsIndexPage(Page):
    template = "news.html"

    parent_page_types = ['home.HomePage']
    subpage_types = ['news.NewsDetailPage']
    max_count = 1

    description = models.TextField(blank=True)
    hero = StreamField(
        [
            ('video_jumbotron', VideoJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('hero'),
    ]

    class Meta:
        verbose_name = "News index page"


class NewsDetailPage(Page):
    parent_page_types = ['news.NewsIndexPage']

    publication_date = models.DateField()

    main_media = StreamField(
        [
            ('video', VideoChooserBlock()),
            ('image', ImageChooserBlock()),
        ],
        max_num=1,
        use_json_field=True
    )

    body = StreamField(
        [
            ('paragraph', RichTextBlock(features=['bold', 'italic', 'link'])),
            ('image', ImageChooserBlock()),
        ],
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('main_media'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "News detail page"