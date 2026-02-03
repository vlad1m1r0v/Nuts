from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from core.validators import ukrainian_phone_validator, validate_file_size
from locations.models import Country, Region
from users.validators import full_name_validator


class BaseRegistrationForm(forms.Form):
    # Contacts
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "ФИО*"}),
        min_length=10,
        max_length=60,
        label="ФИО",
        validators=[full_name_validator],
        error_messages={
            "required": "ФИО поле обязательное для заполнения.",
            "max_length": "ФИО поле может местить максимум 60 символов.",
            "min_length": "ФИО поле должно местить минимум 10 символов."
        }
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "E-Mail*"}),
        label="E-Mail",
        error_messages={
            "required": "E-Mail поле обязательное для заполнения.",
            "invalid": "E-Mail не валидний."
        }
    )
    phone = forms.CharField(
        widget=forms.TelInput(attrs={"placeholder": "Телефон*"}),
        label="Телефон",
        validators=[ukrainian_phone_validator],
        error_messages={
            "required": "Телефон поле обязательное для заполнения."
        }
    )
    # Address
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label="Страна",
        label="Страна",
        error_messages={
            "required": "Страна поле обязательное для заполнения."
        }
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label="Область",
        label="Область",
        error_messages={
            "required": "Область поле обязательное для заполнения."
        }
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
    address_line = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Адрес"}),
        min_length=20,
        max_length=100,
        label="Адрес",
        required=False,
        error_messages={
            "max_length": "Адрес поле может местить максимум 100 символов.",
            "min_length": "Адрес поле должно местить минимум 20 символов."
        }
    )
    # Password and confirm password
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Пароль*"
        }),
        label="Пароль",
        error_messages={
            "required": "Пароль поле обязательное для заполнения."
        }
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Подтвердите пароль*"
        }),
        label="Подтвердите пароль",
        error_messages={
            "required": "Подтвердите пароль поле обязательное для заполнения."
        }
    )
    # Agreed to terms
    agreed_to_terms = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "checkbox-custom", "id": "checkbox-2"}),
        label="Согласие с условиями",
        error_messages={
            "required": "Согласие с условиями поле обязательное для заполнения."
        }
    )
    # Avatar
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={
            "id": "file2",
            "class": "inputfile"
        }),
        label="Аватар",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']),
            validate_file_size
        ],
        error_messages={
            'required': 'Аватар поле обязательное для заполнения.',
            'invalid_image': 'Загруженный файл не является изображением или поврежден.',
        }
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError:
            raise ValidationError(
                "Ваш пароль не соответствует требованиям безопасности.")
        return password

    def clean(self):
        cleaned_data = super().clean()

        country = cleaned_data.get("country")
        region = cleaned_data.get("region")

        if region.country_id != country.pk:
            raise ValidationError("Выбранная область не принадлежит указанной стране.")

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if all([password, password_confirm]) and password != password_confirm:
            raise ValidationError("Пароли не совпадают.")

        return cleaned_data


class IndividualRegistrationForm(BaseRegistrationForm):
    is_fop = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "checkbox-custom", "id": "checkbox-1"}),
        required=False,
        label="Являюсь ФОП"
    )
