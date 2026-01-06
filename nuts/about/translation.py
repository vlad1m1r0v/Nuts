from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import AboutPage

@register(AboutPage)
class AboutPageTR(TranslationOptions):
    fields = (
        'description',
        'owner_cite',
        'owner_description',
        'write_us',
        'company_history_title',
        'company_history_description',
    )