from django.db import models
from django.utils.html import strip_tags

from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from wagtailmedia.blocks import VideoChooserBlock

from core.blocks import VideoJumbotronBlock


class NewsIndexPage(Page):
    template = "news_index.html"

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
    template = "news_detail.html"

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
            ('paragraph', RichTextBlock()),
            ('image', ImageChooserBlock()),
        ],
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('main_media'),
        FieldPanel('body'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        latest_news = NewsDetailPage.objects.live().public().not_page(self).order_by('-publication_date')[:5]
        context['latest_news'] = latest_news

        return context

    def get_excerpt(self):
        full_text = ""

        for block in self.body:
            if block.block_type == 'paragraph':
                full_text += strip_tags(block.value.source) + " "

        excerpt = full_text.strip()
        if len(excerpt) > 200:
            excerpt = excerpt[:197] + "..."

        return excerpt

    class Meta:
        verbose_name = "News detail page"
