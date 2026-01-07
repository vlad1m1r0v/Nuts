from modeltranslation.translator import register, TranslationOptions
from .models import PaymentAndDeliveryPage

@register(PaymentAndDeliveryPage)
class PaymentAndDeliveryPageTR(TranslationOptions):
    fields = (
        'image_hero',
        'payment_info',
        'delivery_info',
        'return_info',
        'video_hero'
    )
