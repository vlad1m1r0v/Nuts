from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import ProductPage, Product, ProductFeature


@register(ProductPage)
class ProductPageTR(TranslationOptions):
    fields = (
        "storage_conditions",
        "description_info",
        "packaging_info",
        "payment_info",
        "delivery_info"
    )

@register(ProductFeature)
class ProductFeatureTR(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTR(TranslationOptions):
    fields = (
        'name',
        'ingredients',
    )