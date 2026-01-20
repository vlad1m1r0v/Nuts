from django.db import models
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from wagtailmedia.blocks import VideoChooserBlock

from core.blocks import VideoJumbotronBlock

from .blocks import GalleryImageWithTextBlock


class GalleryPage(Page):
    template = "gallery.html"
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1

    hero = StreamField(
        [
            ('video_jumbotron', VideoJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1
    )

    subtitle = models.CharField(
        max_length=255,
        blank=True,
    )

    content = StreamField(
        [
            ('video', VideoChooserBlock()),
            ('image_with_text', GalleryImageWithTextBlock()),
            ('video_jumbotron', VideoJumbotronBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('hero'),
        FieldPanel('content'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        all_blocks = self.content

        paginator = Paginator(all_blocks, 5)
        page_number = request.GET.get('page', 1)
        blocks_page = paginator.get_page(page_number)

        context['blocks'] = blocks_page
        return context

    def serve(self, request, *args, **kwargs):
        if request.headers.get('HX-Request'):
            context = self.get_context(request)

            return TemplateResponse(
                request,
                "includes/gallery/blocks.html",
                context
            )
        # Звичайний запит
        return super().serve(request)

    class Meta:
        verbose_name = "Gallery page"
