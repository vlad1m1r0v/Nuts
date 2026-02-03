from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from core.validators import ukrainian_phone_validator, validate_file_size

from locations.models import Country, Region

from users.validators import full_name_validator
from users.models import BusinessProfile

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
        widget=forms.CheckboxInput(attrs={"class": "checkbox-custom", "id": "individual_terms"}),
        label="Согласие с условиями",
        error_messages={
            "required": "Согласие с условиями поле обязательное для заполнения."
        }
    )
    # Avatar
    avatar = forms.ImageField(
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


class BusinessRegistrationForm(BaseRegistrationForm):
    # Avatar
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={
            "id": "business_avatar_file",
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
    # Agreed to terms
    agreed_to_terms = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "checkbox-custom", "id": "business_terms"}),
        label="Согласие с условиями",
        error_messages={
            "required": "Согласие с условиями поле обязательное для заполнения."
        }
    )


    business_type = forms.ChoiceField(
        choices=[('ur', 'Юридическое лицо'), ('fop', 'ФОП')],
        widget=forms.RadioSelect(attrs={'class': 'radio-custom'}),
        initial='ur',
        label="Тип бизнеса"
    )

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
        label="ЕДРПО",
        widget=forms.TextInput(attrs={"placeholder": "ЕДРПО"}),
        error_messages={"max_length": "ЕДРПО поле может местить максимум 32 символа."}
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
            "max_length": "Город (юр.) поле может местить максимум 30 символов.",
            "min_length": "Город (юр.) поле должно местить минимум 3 символа."
        }
    )
    legal_address_line = forms.CharField(
        required=False,
        min_length=10,
        max_length=100,
        label="Адрес (юр.)",
        widget=forms.TextInput(attrs={"placeholder": "Адрес"}),
        error_messages={
            "max_length": "Адрес (юр.) поле может местить максимум 100 символов.",
            "min_length": "Адрес (юр.) поле должно местить минимум 10 символов."
        }
    )
    legal_index = forms.CharField(
        required=False,
        min_length=5,
        max_length=10,
        label="Индекс (юр.)",
        widget=forms.TextInput(attrs={"placeholder": "Индекс"}),
        error_messages={
            "max_length": "Индекс (юр.) поле может местить максимум 10 символов.",
            "min_length": "Индекс (юр.) поле должно местить минимум 5 символов."
        }
    )

    fop_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Страна (деятельности)",
        empty_label="Страна"
    )
    fop_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Область (деятельности)",
        empty_label="Область"
    )
    fop_city = forms.CharField(
        required=False,
        min_length=3,
        max_length=30,
        label="Город (деятельности)",
        widget=forms.TextInput(attrs={"placeholder": "Город*"}),
        error_messages={
            "max_length": "Город (деятельности) поле может местить максимум 30 символов.",
            "min_length": "Город (деятельности) поле должно местить минимум 3 символа."
        }
    )
    fop_address_line = forms.CharField(
        required=False,
        min_length=10,
        max_length=100,
        label="Адрес (деятельности)",
        widget=forms.TextInput(attrs={"placeholder": "Адрес"}),
        error_messages={
            "max_length": "Адрес (деятельности) поле может местить максимум 100 символов.",
            "min_length": "Адрес (деятельности) поле должно местить минимум 10 символов."
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        b_type = cleaned_data.get('business_type')

        if b_type == BusinessProfile.BusinessType.LEGAL_ENTITY:
            self._validate_required_fields(cleaned_data, [
                ('okpo', 'ОКПО'),
                ('legal_country', 'Страна (юр.)'),
                ('legal_region', 'Область (юр.)'),
                ('legal_city', 'Город (юр.)')
            ])

            l_country = cleaned_data.get('legal_country')
            l_region = cleaned_data.get('legal_region')
            if l_country and l_region and l_region.country_id != l_country.pk:
                self.add_error('legal_region', "Область (юр.) поле: Выбранная область не принадлежит указанной стране.")

        elif b_type == BusinessProfile.BusinessType.FOP:
            self._validate_required_fields(cleaned_data, [
                ('edrpo', 'ЕДРПО'),
                ('fop_country', 'Страна (деятельности)'),
                ('fop_region', 'Область (деятельности)'),
                ('fop_city', 'Город (деятельности)')
            ])

            f_country = cleaned_data.get('fop_country')
            f_region = cleaned_data.get('fop_region')
            if f_country and f_region and f_region.country_id != f_country.pk:
                self.add_error('fop_region',
                               "Область (деятельности) поле: Выбранная область не принадлежит указанной стране.")

        return cleaned_data

    def _validate_required_fields(self, cleaned_data, fields_with_labels):
        for field_name, label in fields_with_labels:
            if not cleaned_data.get(field_name):
                self.add_error(field_name, f"{label} поле обязательное для заполнения.")


