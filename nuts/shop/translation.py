from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import ShopPage

@register(ShopPage)
class ShopPageTR(TranslationOptions):
    fields = (
        'hero',
        'nut_title',
        'nut_description',
        'gallery'
    )