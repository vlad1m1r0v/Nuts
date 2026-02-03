from django.db import models
from django.utils.html import strip_tags
from django.template.response import TemplateResponse
from django.core.paginator import Paginator

from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from wagtailmedia.blocks import VideoChooserBlock

from core.blocks import VideoJumbotronBlock


class NewsIndexPage(Page):
    template = "news/news_index.html"

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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        all_news = NewsDetailPage.objects.child_of(self).live().order_by('-publication_date')

        paginator = Paginator(all_news, 1)
        page_number = request.GET.get('page', 1)
        news_page = paginator.get_page(page_number)

        context['news_list'] = news_page
        context['hero'] = self.hero

        return context

    def serve(self, request, *args, **kwargs):
        if request.headers.get('HX-Request'):
            context = self.get_context(request)
            return TemplateResponse(
                request,
                "includes/news/list.html",
                context
            )

        return super().serve(request)

    class Meta:
        verbose_name = "News index page"


class NewsDetailPage(Page):
    template = "news/news_detail.html"

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
        if len(excerpt) > 300:
            excerpt = excerpt[:297] + "..."

        return excerpt

    class Meta:
        verbose_name = "News detail page"
