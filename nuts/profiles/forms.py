from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from core.validators import ukrainian_phone_validator, validate_file_size

from users.models import CustomerProfile
from users.validators import full_name_validator


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