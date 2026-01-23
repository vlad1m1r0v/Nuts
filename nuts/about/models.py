from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image

from wagtailmedia.blocks import VideoChooserBlock

from core.blocks import VideoJumbotronBlock, ImageJumbotronBlock

from gallery.models import GalleryPage
from news.models import NewsIndexPage, NewsDetailPage


class AboutPage(Page):
    template = "about.html"

    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    description = models.TextField(blank=True)

    hero = StreamField(
        [
            ("video_jumbotron", VideoJumbotronBlock()),
        ],
        blank=True,
        use_json_field=True,
        max_num=1
    )

    videos = StreamField([
        ('video', VideoChooserBlock())
    ], blank=True, use_json_field=True)

    owner_name = models.CharField(max_length=100, null=True, blank=True)
    owner_photo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    owner_cite = models.CharField(max_length=255, blank=True)
    owner_description = models.TextField(blank=True)

    company_history_title = models.CharField(max_length=255, blank=True)
    company_history_description = models.TextField(blank=True)

    image_hero = StreamField(
        [
            ("image_jumbotron", ImageJumbotronBlock()),
        ],
        blank=True,
        use_json_field=True,
        max_num=1
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("hero"),
        FieldPanel("videos"),
        FieldPanel("owner_name"),
        FieldPanel("owner_photo"),
        FieldPanel("owner_cite"),
        FieldPanel("owner_description"),
        FieldPanel("company_history_title"),
        FieldPanel("company_history_description"),
        FieldPanel("image_hero"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context["gallery_page"] = GalleryPage.objects.live().first()
        context["news_page"] = NewsIndexPage.objects.live().first()
        context["news_list"] = NewsDetailPage.objects.live().order_by('-publication_date')[:3]

        return context

    class Meta:
        verbose_name = "About page"
