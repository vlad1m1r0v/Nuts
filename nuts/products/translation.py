from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import ProductPage


@register(ProductPage)
class ProductPageTR(TranslationOptions):
    fields = (
        "storage_conditions",
        "description_info",
        "packaging_info",
        "payment_info",
        "delivery_info"
    )