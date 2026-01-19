from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import RegisterPage, TermsOfUsePage

@register(RegisterPage)
class RegisterPageTR(TranslationOptions):
    pass

@register(TermsOfUsePage)
class TermsOfUsePageTR(TranslationOptions):
    fields = (
        'description',
    )