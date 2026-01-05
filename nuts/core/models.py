from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import register_setting
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.images.models import Image
from wagtail.fields import StreamField

from .validators import ukrainian_phone_validator
from .blocks import StatisticItemBlock


@register_setting
class CompanySettings(BaseSiteSetting):
    company_name = models.CharField(max_length=100, blank=True)

    logo = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        blank=True
    )

    header_text = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Company settings'


@register_setting
class DiscountBannerSettings(BaseSiteSetting):
    is_enabled = models.BooleanField(default=False)
    text = models.CharField(max_length=100, blank=True)
    discount_percent = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Discount banner settings'


@register_setting
class ContactSettings(BaseSiteSetting):
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    whatsapp_url = models.URLField(null=True, blank=True)
    telegram_url = models.URLField(null=True, blank=True)
    viber_url = models.URLField(null=True, blank=True)

    _tab_socials = [
        FieldPanel('facebook_url'),
        FieldPanel('instagram_url'),
        FieldPanel('youtube_url'),
        FieldPanel('whatsapp_url'),
        FieldPanel('telegram_url'),
        FieldPanel('viber_url'),
    ]

    manager_name = models.CharField(max_length=100, null=True, blank=True)
    manager_phone = models.CharField(
        max_length=20,
        validators=[ukrainian_phone_validator],
        null=True,
        blank=True
    )

    _tab_manager = [
        FieldPanel('manager_name'),
        FieldPanel('manager_phone'),
    ]

    phone_1 = models.CharField(
        max_length=20,
        validators=[ukrainian_phone_validator],
        null=True,
        blank=True
    )
    phone_2 = models.CharField(
        max_length=20,
        validators=[ukrainian_phone_validator],
        null=True,
        blank=True
    )

    _tab_phones = [
        FieldPanel('phone_1'),
        FieldPanel('phone_2')
    ]

    email = models.EmailField(null=True, blank=True)

    _tab_email = [
        FieldPanel('email'),
    ]

    office_and_sales_department_address = models.TextField(null=True, blank=True)
    production_address = models.TextField(null=True, blank=True)

    _tab_addresses = [
        FieldPanel('office_and_sales_department_address'),
        FieldPanel('production_address')
    ]

    map_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    map_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    _tab_map = [
        FieldPanel('map_latitude'),
        FieldPanel('map_longitude'),
    ]

    panels = [
            MultiFieldPanel(_tab_socials, heading='Social Networks'),
            MultiFieldPanel(_tab_manager, heading='Manager'),
            MultiFieldPanel(_tab_phones, heading='Phones'),
            MultiFieldPanel(_tab_email, heading='Email'),
            MultiFieldPanel(_tab_addresses, heading='Addresses'),
            MultiFieldPanel(_tab_map, heading='Map')
    ]

    class Meta:
        verbose_name = 'Contact settings'


@register_setting
class StatisticsSettings(BaseSiteSetting):
    items = StreamField(
        [
            ('item', StatisticItemBlock()),
        ],
        use_json_field=True,
    )

    class Meta:
        verbose_name = 'Statistics settings'
