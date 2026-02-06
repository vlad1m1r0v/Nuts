from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import AddressPage

@register(AddressPage)
class AddressPageTR(TranslationOptions):
    fields = (
        'side_image_title',
        'side_image_description'
    )