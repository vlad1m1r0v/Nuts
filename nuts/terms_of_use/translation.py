from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import TermsOfUsePage

@register(TermsOfUsePage)
class TermsOfUseTR(TranslationOptions):
    fields = (
        'description',
    )