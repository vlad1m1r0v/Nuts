from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from core.validators import ukrainian_phone_validator, validate_file_size

from users.models import CustomerProfile, BusinessProfile
from users.validators import full_name_validator

from locations.models import Region, Country


class BaseContactInformationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "E-Mail*"}),
        label="E-Mail",
        error_messages={
            "required": "E-Mail поле обязательное для заполнения.",
            "invalid": "E-Mail не валидный."
        }
    )
    phone = forms.CharField(
        widget=forms.TelInput(attrs={"placeholder": "Телефон*"}),
        label="Телефон",
        validators=[ukrainian_phone_validator],
        error_messages={"required": "Телефон поле обязательное для заполнения."}
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
            'invalid_image': 'Загруженный файл не является изображением или поврежден.',
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
            raise ValidationError("Пользователь с таким E-Mail уже зарегистрирован.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        qs = CustomerProfile.objects.filter(phone=phone)
        if self.user and hasattr(self.user, 'customer_profile'):
            qs = qs.exclude(pk=self.user.customer_profile.pk)
        if qs.exists():
            raise ValidationError("Пользователь с таким номером телефона уже зарегистрирован.")
        return phone


class IndividualContactInformationForm(BaseContactInformationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "ФИО*"}),
        min_length=10,
        max_length=60,
        label="ФИО",
        validators=[full_name_validator],
        error_messages={
            "required": "ФИО поле обязательное для заполнения.",
            "min_length": "ФИО должно содержать минимум 10 символов.",
            "max_length": "ФИО не может превышать 60 символов."
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
        widget=forms.TextInput(attrs={"placeholder": "Название компании*"}),
        min_length=3,
        max_length=60,
        label="Компания",
        error_messages={
            "required": "Название компании обязательно для заполнения.",
            "min_length": "Название компании слишком короткое.",
            "max_length": "Название компании не может превышать 60 символов."
        }
    )

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Контактное лицо*"}),
        min_length=10,
        max_length=60,
        label="ФИО",
        validators=[full_name_validator],
        error_messages={
            "required": "Укажите контактное лицо.",
            "min_length": "ФИО контактного лица слишком короткое.",
            "max_length": "ФИО не может превышать 60 символов."
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
        empty_label="Страна",
        label="Страна",
        error_messages={"required": "Страна поле обязательное для заполнения."}
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label="Область",
        label="Область",
        error_messages={"required": "Область поле обязательное для заполнения."}
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Город*"}),
        min_length=3,
        max_length=30,
        label="Город",
        error_messages={
            "required": "Город поле обязательное для заполнения.",
            "max_length": "Город поле может местить максимум 30 символов.",
            "min_length": "Город поле должно местить минимум 3 символа."
        }
    )
    street_address = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Адрес (улица, дом, кв.)*"}),
        min_length=10,
        max_length=100,
        label="Адрес",
        error_messages={
            "required": "Адрес поле обязательное для заполнения.",
            "max_length": "Адрес поле может местить максимум 100 символов.",
            "min_length": "Адрес поле должно местить минимум 10 символов."
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
            self.add_error('region', "Выбранная область не принадлежит указанной стране.")
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
        error_messages={"max_length": "ОКПО поле может местить максимум 32 символа."}
    )
    edrpo = forms.CharField(
        required=False,
        max_length=32,
        label="ЕДРПОУ",
        widget=forms.TextInput(attrs={"placeholder": "ЕДРПОУ"}),
        error_messages={"max_length": "ЕДРПОУ поле может местить максимум 32 символа."}
    )

    legal_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Страна (юр.)",
        empty_label="Страна"
    )
    legal_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Область (юр.)",
        empty_label="Область"
    )
    legal_city = forms.CharField(
        required=False,
        min_length=3,
        max_length=30,
        label="Город (юр.)",
        widget=forms.TextInput(attrs={"placeholder": "Город*"}),
        error_messages={
            "max_length": "Город поле может местить максимум 30 символов.",
            "min_length": "Город поле должно местить минимум 3 символа."
        }
    )
    legal_address_line = forms.CharField(
        required=False,
        min_length=10,
        max_length=100,
        label="Адрес (юр.)",
        widget=forms.TextInput(attrs={"placeholder": "Адрес"}),
        error_messages={
            "max_length": "Адрес поле может местить максимум 100 символов.",
            "min_length": "Адрес поле должно местить минимум 10 символов."
        }
    )
    legal_index = forms.CharField(
        required=False,
        min_length=5,
        max_length=10,
        label="Индекс (юр.)",
        widget=forms.TextInput(attrs={"placeholder": "Индекс"}),
        error_messages={
            "max_length": "Индекс поле может местить максимум 10 символов.",
            "min_length": "Индекс поле должно местить минимум 5 символов."
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        biz_profile = self.user.customer_profile.business_profile
        b_type = biz_profile.business_type

        if b_type == BusinessProfile.BusinessType.LEGAL_ENTITY:
            self._validate_required_fields(cleaned_data, [
                ('okpo', 'ОКПО'),
                ('legal_country', 'Страна (юр.)'),
                ('legal_region', 'Область (юр.)'),
                ('legal_city', 'Город (юр.)'),
                ('legal_address_line', 'Адрес (юр.)'),
                ('legal_index', 'Индекс (юр.)')
            ])
        else:
            self._validate_required_fields(cleaned_data, [
                ('edrpo', 'ЕДРПОУ'),
                ('legal_country', 'Страна (деятельности)'),
                ('legal_region', 'Область (деятельности)'),
                ('legal_city', 'Город (деятельности)'),
                ('legal_address_line', 'Адрес (деятельности)'),
                ('legal_index', 'Индекс (деятельности)')
            ])

        l_country = cleaned_data.get('legal_country')
        l_region = cleaned_data.get('legal_region')
        if l_country and l_region and l_region.country_id != l_country.pk:
            self.add_error('legal_region', "Выбранная область не принадлежит указанной стране.")

        return cleaned_data

    def _validate_required_fields(self, cleaned_data, fields_with_labels):
        for field_name, label in fields_with_labels:
            if not cleaned_data.get(field_name):
                self.add_error(field_name, f"{label} поле обязательное для заполнения.")

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
        widget=forms.PasswordInput(attrs={"placeholder": "Текущий пароль*"}),
        label="Текущий пароль",
        error_messages={"required": "Введите текущий пароль."}
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Новый пароль*"}),
        label="Новый пароль",
        error_messages={"required": "Введите новый пароль."}
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Подтвердить пароль*"}),
        label="Подтвердите пароль",
        error_messages={"required": "Подтвердите новый пароль."}
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise ValidationError("Текущий пароль введён неверно.")
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')

        try:
            validate_password(new_password)
        except ValidationError:
            raise ValidationError(
                "Ваш пароль не соответствует требованиям безопасности."
            )
        return new_password

    def clean(self):
        cleaned_data = super().clean()

        new_p = cleaned_data.get("new_password")
        conf_p = cleaned_data.get("confirm_password")

        if new_p and conf_p and new_p != conf_p:
            raise ValidationError("Новые пароли не совпадают.")

        if new_p and cleaned_data.get("old_password") == new_p:
            raise ValidationError("Новый пароль не должен совпадать со старым.")

        return cleaned_data