from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import NotFoundPage


@register(NotFoundPage)
class NotFoundPageTR(TranslationOptions):
    fields = (
        'hero_text',
        'subtitle',
        'button_text'
    )
