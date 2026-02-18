from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from core.validators import ukrainian_phone_validator, validate_file_size

from users.models import CustomerProfile, BusinessProfile
from users.validators import full_name_validator

from locations.models import Region, Country


class BaseContactInformationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("E-Mail*")}),
        label="E-Mail",
        error_messages={
            "required": _("E-Mail поле обязательное для заполнения."),
            "invalid": _("E-Mail не валидный.")
        }
    )
    phone = forms.CharField(
        widget=forms.TelInput(attrs={"placeholder": _("Телефон*")}),
        label="Телефон",
        validators=[ukrainian_phone_validator],
        error_messages={"required": _("Телефон поле обязательное для заполнения.")}
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "id": "individual_avatar_file",
            "class": "inputfile"
        }),
        label="Аватар",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']),
            validate_file_size
        ],
        error_messages={
            'invalid_image': _("Загруженный файл не является изображением или поврежден."),
        }
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise ValidationError(_("Пользователь с таким E-Mail уже зарегистрирован."))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        qs = CustomerProfile.objects.filter(phone=phone)
        if self.user and hasattr(self.user, 'customer_profile'):
            qs = qs.exclude(pk=self.user.customer_profile.pk)
        if qs.exists():
            raise ValidationError(_("Пользователь с таким номером телефона уже зарегистрирован."))
        return phone


class IndividualContactInformationForm(BaseContactInformationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("ФИО*")}),
        min_length=10,
        max_length=60,
        label="ФИО",
        validators=[full_name_validator],
        error_messages={
            "required": _("ФИО поле обязательное для заполнения."),
            "min_length": _("ФИО должно содержать минимум 10 символов."),
            "max_length": _("ФИО не может превышать 60 символов.")
        }
    )

    def save(self):
        user = self.user
        profile = user.customer_profile
        data = self.cleaned_data

        user.email = data['email']
        user.username = data['full_name']
        user.save()

        profile.phone = data['phone']
        profile.full_name = data['full_name']

        if data.get("avatar"):
            profile.avatar = data['avatar']

        profile.save()


class LegalEntityContactInformationForm(BaseContactInformationForm):
    company_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Название компании*")}),
        min_length=3,
        max_length=60,
        label="Компания",
        error_messages={
            "required": _("Название компании обязательно для заполнения."),
            "min_length": _("Название компании слишком короткое."),
            "max_length": _("Название компании не может превышать 60 символов.")
        }
    )

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Контактное лицо*")}),
        min_length=10,
        max_length=60,
        label="ФИО",
        validators=[full_name_validator],
        error_messages={
            "required": _("Укажите контактное лицо."),
            "min_length": _("ФИО контактного лица слишком короткое."),
            "max_length": _("ФИО не может превышать 60 символов.")
        }
    )

    def save(self):
        user = self.user
        profile = user.customer_profile
        data = self.cleaned_data

        user.email = data['email']
        user.username = data['full_name']
        user.save()

        profile.phone = data['phone']
        profile.full_name = data['full_name']
        profile.company_name = data['company_name']

        if data.get("avatar"):
            profile.avatar = data['avatar']

        profile.save()


class BaseAddressForm(forms.Form):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label=_("Страна"),
        label="Страна",
        error_messages={"required": _("Страна поле обязательное для заполнения.")}
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label=_("Область"),
        label="Область",
        error_messages={"required": _("Область поле обязательное для заполнения.")}
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Город*")}),
        min_length=3,
        max_length=30,
        label="Город",
        error_messages={
            "required": _("Город поле обязательное для заполнения."),
            "max_length": _("Город поле может местить максимум 30 символов."),
            "min_length": _("Город поле должно местить минимум 3 символа.")
        }
    )
    street_address = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Адрес (улица, дом, кв.)*")}),
        min_length=10,
        max_length=100,
        label="Адрес",
        error_messages={
            "required": _("Адрес поле обязательное для заполнения."),
            "max_length": _("Адрес поле может местить максимум 100 символов."),
            "min_length": _("Адрес поле должно местить минимум 10 символов.")
        }
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get("country")
        region = cleaned_data.get("region")

        if country and region and region.country_id != country.pk:
            self.add_error('region', _("Выбранная область не принадлежит указанной стране."))
        return cleaned_data


class IndividualAddressForm(BaseAddressForm):
    def save(self):
        profile = self.user.customer_profile
        addr = profile.contact_address
        data = self.cleaned_data

        addr.region = data['region']
        addr.city = data['city']
        addr.street_address = data['street_address']
        addr.save()
        return addr


class BusinessAddressForm(BaseAddressForm):
    okpo = forms.CharField(
        required=False,
        max_length=32,
        label="ОКПО",
        widget=forms.TextInput(attrs={"placeholder": "ОКПО"}),
        error_messages={"max_length": _("ОКПО поле может местить максимум 32 символа.")}
    )
    edrpo = forms.CharField(
        required=False,
        max_length=32,
        label="ЕДРПОУ",
        widget=forms.TextInput(attrs={"placeholder": "ЕДРПОУ"}),
        error_messages={"max_length": _("ЕДРПОУ поле может местить максимум 32 символа.")}
    )

    legal_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Страна (юр.)",
        empty_label=_("Страна")
    )
    legal_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Область (юр.)",
        empty_label=_("Область")
    )
    legal_city = forms.CharField(
        required=False,
        min_length=3,
        max_length=30,
        label="Город (юр.)",
        widget=forms.TextInput(attrs={"placeholder": _("Город*")}),
        error_messages={
            "max_length": _("Город поле может местить максимум 30 символов."),
            "min_length": _("Город поле должно местить минимум 3 символа.")
        }
    )
    legal_address_line = forms.CharField(
        required=False,
        min_length=10,
        max_length=100,
        label="Адрес (юр.)",
        widget=forms.TextInput(attrs={"placeholder": _("Адрес")}),
        error_messages={
            "max_length": _("Адрес поле может местить максимум 100 символов."),
            "min_length": _("Адрес поле должно местить минимум 10 символов.")
        }
    )
    legal_index = forms.CharField(
        required=False,
        min_length=5,
        max_length=10,
        label="Индекс (юр.)",
        widget=forms.TextInput(attrs={"placeholder": _("Индекс")}),
        error_messages={
            "max_length": _("Индекс поле может местить максимум 10 символов."),
            "min_length": _("Индекс поле должно местить минимум 5 символов.")
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        biz_profile = self.user.customer_profile.business_profile
        b_type = biz_profile.business_type

        if b_type == BusinessProfile.BusinessType.LEGAL_ENTITY:
            self._validate_required_fields(cleaned_data, [
                ('okpo', _("ОКПО")),
                ('legal_country', _("Страна (юр.)")),
                ('legal_region', _("Область (юр.)")),
                ('legal_city', _("Город (юр.)")),
                ('legal_address_line', _("Адрес (юр.)")),
                ('legal_index', _("Индекс (юр.)"))
            ])
        else:
            self._validate_required_fields(cleaned_data, [
                ('edrpo', _("ЕДРПОУ")),
                ('legal_country', _("Страна (деятельности)")),
                ('legal_region', _("Область (деятельности)")),
                ('legal_city', _("Город (деятельности)")),
                ('legal_address_line', _("Адрес (деятельности)")),
                ('legal_index', _("Индекс (деятельности)"))
            ])

        l_country = cleaned_data.get('legal_country')
        l_region = cleaned_data.get('legal_region')
        if l_country and l_region and l_region.country_id != l_country.pk:
            self.add_error('legal_region', _("Выбранная область не принадлежит указанной стране."))

        return cleaned_data

    def _validate_required_fields(self, cleaned_data, fields_with_labels):
        for field_name, label in fields_with_labels:
            if not cleaned_data.get(field_name):
                self.add_error(field_name, _("%(label)s поле обязательное для заполнения.") % {'label': label})

    def save(self):
        profile = self.user.customer_profile
        biz_profile = profile.business_profile
        data = self.cleaned_data

        c_addr = profile.contact_address
        c_addr.region = data['region']
        c_addr.city = data['city']
        c_addr.street_address = data['street_address']
        c_addr.save()

        if biz_profile.business_type == BusinessProfile.BusinessType.LEGAL_ENTITY:
            details = biz_profile.legal_details
            details.okpo_code = data['okpo']
            b_addr = details.legal_address
        else:
            details = biz_profile.fop_details
            details.edrpo_code = data['edrpo']
            b_addr = details.activity_address

        b_addr.region = data['legal_region']
        b_addr.city = data['legal_city']
        b_addr.street_address = data['legal_address_line']
        b_addr.postal_code = data['legal_index']

        b_addr.save()
        details.save()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Текущий пароль*")}),
        label="Текущий пароль",
        error_messages={"required": _("Введите текущий пароль.")}
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Новый пароль*")}),
        label="Новый пароль",
        error_messages={"required": _("Введите новый пароль.")}
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Подтвердить пароль*")}),
        label="Подтвердите пароль",
        error_messages={"required": _("Подтвердите новый пароль.")}
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise ValidationError(_("Текущий пароль введён неверно."))
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')

        try:
            validate_password(new_password)
        except ValidationError:
            raise ValidationError(
                _("Ваш пароль не соответствует требованиям безопасности.")
            )
        return new_password

    def clean(self):
        cleaned_data = super().clean()

        new_p = cleaned_data.get("new_password")
        conf_p = cleaned_data.get("confirm_password")

        if new_p and conf_p and new_p != conf_p:
            raise ValidationError(_("Новые пароли не совпадают."))

        if new_p and cleaned_data.get("old_password") == new_p:
            raise ValidationError(_("Новый пароль не должен совпадать со старым."))

        return cleaned_data