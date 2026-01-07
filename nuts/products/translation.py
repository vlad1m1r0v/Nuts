from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import ProductCommonSettings


@register(ProductCommonSettings)
class ProductCommonSettingsTR(TranslationOptions):
    fields = (
        "storage_conditions",
        "description_info",
        "packaging_info",
        "payment_info",
        "delivery_info"
    )