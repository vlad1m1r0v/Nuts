from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from core.validators import ukrainian_phone_validator
from locations.models import Address

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', verbose_name="Пользователь")
    company_name = models.CharField(max_length=60, verbose_name="Компания", null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Аватар")
    full_name = models.CharField(max_length=60, verbose_name="ФИО")
    phone = models.CharField(unique=True, verbose_name="Номер телефона", validators=[ukrainian_phone_validator])
    contact_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='customer_contacts', verbose_name="Контактный адрес")
    agreed_to_terms = models.BooleanField(default=False, verbose_name="Согласие с условиями")
    is_fop = models.BooleanField(default=False, verbose_name="Является ли ФОП")

    class Meta:
        verbose_name = "Профиль клиента"
        verbose_name_plural = "Профили клиентов"

    def __str__(self):
        return self.full_name


class BusinessProfile(models.Model):
    class BusinessType(models.TextChoices):
        LEGAL_ENTITY = 'LEGAL_ENTITY', _("Юридическое лицо")
        FOP = 'FOP', _("ФОП")

    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='business_profile', verbose_name="Профиль клиента")
    business_type = models.CharField(
        max_length=16,
        choices=BusinessType,
        default=BusinessType.LEGAL_ENTITY,
        verbose_name="Тип бизнеса"
    )

    class Meta:
        verbose_name = "Бизнес профиль"
        verbose_name_plural = "Бизнес профили"


class LegalEntityDetails(models.Model):
    business = models.OneToOneField(BusinessProfile, on_delete=models.CASCADE, related_name='legal_details', verbose_name="Бизнес профиль")
    legal_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='legal_entities', verbose_name="Юридический адрес")
    okpo_code = models.CharField(max_length=32, verbose_name="Код ОКПО")

    class Meta:
        verbose_name = "Детали юр. лица"
        verbose_name_plural = "Детали юр. лиц"


class FOPDetails(models.Model):
    business = models.OneToOneField(BusinessProfile, on_delete=models.CASCADE, related_name='fop_details', verbose_name="Бизнес профиль")
    activity_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='fop_activities', verbose_name="Адрес деятельности")
    edrpo_code = models.CharField(max_length=32, verbose_name="Код ЕГРПОУ")

    class Meta:
        verbose_name = "Детали ФОП"
        verbose_name_plural = "Детали ФОП"