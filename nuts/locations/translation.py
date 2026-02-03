from modeltranslation.translator import register, TranslationOptions

from locations.models import Country, Region

@register(Country)
class CountryModelTR(TranslationOptions):
    fields = ('name',)

@register(Region)
class RegionModelTR(TranslationOptions):
    fields = ('name',)