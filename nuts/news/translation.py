from modeltranslation.translator import register, TranslationOptions
from .models import NewsIndexPage, NewsDetailPage

@register(NewsIndexPage)
class NewsIndexPageTR(TranslationOptions):
    fields = (
        'description',
    )



@register(NewsDetailPage)
class NewsDetailPageTR(TranslationOptions):
    pass
