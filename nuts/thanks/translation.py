from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import ThanksPage

@register(ThanksPage)
class ThanksPageTR(TranslationOptions):
    fields = (
        'hero',
    )