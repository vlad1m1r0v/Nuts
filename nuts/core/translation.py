from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import (
    CompanySettings,
    DiscountBannerSettings,
    ContactSettings,
    StatisticsSettings,
)


@register(CompanySettings)
class CompanySettingsTR(TranslationOptions):
    fields = (
        "company_name",
        "header_text",
    )


@register(DiscountBannerSettings)
class DiscountBannerSettingsTR(TranslationOptions):
    fields = (
        "text",
    )


@register(ContactSettings)
class ContactSettingsTR(TranslationOptions):
    fields = (
        "manager_name",
        "office_and_sales_department_address",
        "production_address",
    )


@register(StatisticsSettings)
class StatisticsSettingsTR(TranslationOptions):
    fields = (
        "items",
    )
