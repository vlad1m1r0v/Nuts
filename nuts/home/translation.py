from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import HomePage


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'video_hero',
        'products_title',
        'products_subtitle',
        'video_hero_2',
        'product_utility_title',
        'product_utility_description',
        'walnut_utility_description',
        'hazelnut_utility_description',
        'rosehip_utility_description',
        'image_hero',
    )