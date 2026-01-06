from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import GalleryPage


@register(GalleryPage)
class GalleryPageTR(TranslationOptions):
    fields = (
        'subtitle',
        'hero',
        'content',
    )