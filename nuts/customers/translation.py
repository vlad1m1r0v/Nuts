from modeltranslation.translator import register, TranslationOptions
from .models import CustomersPage

@register(CustomersPage)
class CustomersPageTR(TranslationOptions):
    fields = (
        'hero',
        'description_column_1',
        'description_column_2',
        'supermarkets',
        'retail_stores',
        'horeca',
        'fitness_clubs',
        'confectionary_bakeries',
        'image_hero'
    )
