from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from core.validators import ukrainian_phone_validator, validate_file_size
from locations.models import Country, Region
from users.validators import full_name_validator
from users.models import BusinessProfile, CustomerProfile


class BaseRegistrationForm(forms.Form):
    # Contacts
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("ФИО*")}),
        min_length=10,
        max_length=60,
        label=_("ФИО"),
        validators=[full_name_validator],
        error_messages={
            "required": _("ФИО поле обязательное для заполнения."),
            "max_length": _("ФИО поле может местить максимум 60 символов."),
            "min_length": _("ФИО поле должно местить минимум 10 символов.")
        }
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("E-Mail*")}),
        label=_("E-Mail"),
        error_messages={
            "required": _("E-Mail поле обязательное для заполнения."),
            "invalid": _("E-Mail не валидний.")
        }
    )
    phone = forms.CharField(
        widget=forms.TelInput(attrs={"placeholder": _("Телефон*")}),
        label=_("Телефон"),
        validators=[ukrainian_phone_validator],
        error_messages={
            "required": _("Телефон поле обязательное для заполнения.")
        }
    )
    # Address
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label=_("Страна"),
        label=_("Страна"),
        error_messages={
            "required": _("Страна поле обязательное для заполнения.")
        }
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label=_("Область"),
        label=_("Область"),
        error_messages={
            "required": _("Область поле обязательное для заполнения.")
        }
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Город*")}),
        min_length=3,
        max_length=30,
        label=_("Город"),
        error_messages={
            "required": _("Город поле обязательное для заполнения."),
            "max_length": _("Город поле может местить максимум 30 символов."),
            "min_length": _("Город поле должно местить минимум 3 символа.")
        }
    )
    address_line = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Адрес")}),
        min_length=20,
        max_length=100,
        label=_("Адрес"),
        required=False,
        error_messages={
            "max_length": _("Адрес поле может местить максимум 100 символов."),
            "min_length": _("Адрес поле должно местить минимум 20 символов.")
        }
    )
    # Password and confirm password
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": _("Пароль*")
        }),
        label=_("Пароль"),
        error_messages={
            "required": _("Пароль поле обязательное для заполнения.")
        }
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": _("Подтвердите пароль*")
        }),
        label=_("Подтвердите пароль"),
        error_messages={
            "required": _("Подтвердите пароль поле обязательное для заполнения.")
        }
    )
    # Agreed to terms
    agreed_to_terms = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "checkbox-custom", "id": "individual_terms"}),
        label=_("Согласие с условиями"),
        error_messages={
            "required": _("Согласие с условиями поле обязательное для заполнения.")
        }
    )
    # Avatar
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={
            "id": "individual_avatar_file",
            "class": "inputfile"
        }),
        label=_("Аватар"), # Додав переклад
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']),
            validate_file_size
        ],
        error_messages={
            'required': _('Аватар поле обязательное для заполнения.'),
            'invalid_image': _('Загруженный файл не является изображением или поврежден.'),
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("E-Mail поле: Пользователь с таким электронным адресом уже зарегистрирован."))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomerProfile.objects.filter(phone=phone).exists():
            raise ValidationError(_("Телефон поле: Пользователь с таким номером телефона уже зарегистрирован."))
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError:
            raise ValidationError(
                _("Ваш пароль не соответствует требованиям безопасности."))
        return password

    def clean(self):
        cleaned_data = super().clean()

        country = cleaned_data.get("country")
        region = cleaned_data.get("region")

        if country and region and region.country_id != country.pk: # Додав перевірку country на None
            raise ValidationError(_("Выбранная область не принадлежит указанной стране."))

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if all([password, password_confirm]) and password != password_confirm:
            raise ValidationError(_("Пароли не совпадают."))

        return cleaned_data


class IndividualRegistrationForm(BaseRegistrationForm):
    is_fop = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "checkbox-custom", "id": "checkbox-1"}),
        required=False,
        label=_("Являюсь ФОП")
    )


class BusinessRegistrationForm(BaseRegistrationForm):
    # Avatar
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={
            "id": "business_avatar_file",
            "class": "inputfile"
        }),
        label=_("Аватар"),
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']),
            validate_file_size
        ],
        error_messages={
            'required': _('Аватар поле обязательное для заполнения.'),
            'invalid_image': _('Загруженный файл не является изображением или поврежден.'),
        }
    )
    # Agreed to terms
    agreed_to_terms = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "checkbox-custom", "id": "business_terms"}),
        label=_("Согласие с условиями"),
        error_messages={
            "required": _("Согласие с условиями поле обязательное для заполнения.")
        }
    )

    business_type = forms.ChoiceField(
        choices=[('ur', _('Юридическое лицо')), ('fop', _('ФОП'))],
        widget=forms.RadioSelect(attrs={'class': 'radio-custom'}),
        initial='ur',
        label=_("Тип бизнеса")
    )

    okpo = forms.CharField(
        required=False,
        max_length=32,
        label=_("ОКПО"),
        widget=forms.TextInput(attrs={"placeholder": _("ОКПО")}),
        error_messages={"max_length": _("ОКПО поле может местить максимум 32 символа.")}
    )
    edrpo = forms.CharField(
        required=False,
        max_length=32,
        label=_("ЕДРПО"),
        widget=forms.TextInput(attrs={"placeholder": _("ЕДРПО")}),
        error_messages={"max_length": _("ЕДРПО поле может местить максимум 32 символа.")}
    )

    legal_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label=_("Страна (юр.)"),
        empty_label=_("Страна")
    )
    legal_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Область (юр.)"),
        empty_label=_("Область")
    )
    legal_city = forms.CharField(
        required=False,
        min_length=3,
        max_length=30,
        label=_("Город (юр.)"),
        widget=forms.TextInput(attrs={"placeholder": _("Город*")}),
        error_messages={
            "max_length": _("Город (юр.) поле может местить максимум 30 символов."),
            "min_length": _("Город (юр.) поле должно местить минимум 3 символа.")
        }
    )
    legal_address_line = forms.CharField(
        required=False,
        min_length=10,
        max_length=100,
        label=_("Адрес (юр.)"),
        widget=forms.TextInput(attrs={"placeholder": _("Адрес")}),
        error_messages={
            "max_length": _("Адрес (юр.) поле может местить максимум 100 символов."),
            "min_length": _("Адрес (юр.) поле должно местить минимум 10 символов.")
        }
    )
    legal_index = forms.CharField(
        required=False,
        min_length=5,
        max_length=10,
        label=_("Индекс (юр.)"),
        widget=forms.TextInput(attrs={"placeholder": _("Индекс")}),
        error_messages={
            "max_length": _("Индекс (юр.) поле может местить максимум 10 символов."),
            "min_length": _("Индекс (юр.) поле должно местить минимум 5 символов.")
        }
    )

    fop_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label=_("Страна (деятельности)"),
        empty_label=_("Страна")
    )
    fop_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Область (деятельности)"),
        empty_label=_("Область")
    )
    fop_city = forms.CharField(
        required=False,
        min_length=3,
        max_length=30,
        label=_("Город (деятельности)"),
        widget=forms.TextInput(attrs={"placeholder": _("Город*")}),
        error_messages={
            "max_length": _("Город (деятельности) поле может местить максимум 30 символов."),
            "min_length": _("Город (деятельности) поле должно местить минимум 3 символа.")
        }
    )
    fop_address_line = forms.CharField(
        required=False,
        min_length=10,
        max_length=100,
        label=_("Адрес (деятельности)"),
        widget=forms.TextInput(attrs={"placeholder": _("Адрес")}),
        error_messages={
            "max_length": _("Адрес (деятельности) поле может местить максимум 100 символов."),
            "min_length": _("Адрес (деятельности) поле должно местить минимум 10 символов.")
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        b_type = cleaned_data.get('business_type')

        if b_type == BusinessProfile.BusinessType.LEGAL_ENTITY:
            self._validate_required_fields(cleaned_data, [
                ('okpo', _('ОКПО')),
                ('legal_country', _('Страна (юр.)')),
                ('legal_region', _('Область (юр.)')),
                ('legal_city', _('Город (юр.)'))
            ])

            l_country = cleaned_data.get('legal_country')
            l_region = cleaned_data.get('legal_region')
            if l_country and l_region and l_region.country_id != l_country.pk:
                self.add_error('legal_region', _("Область (юр.) поле: Выбранная область не принадлежит указанной стране."))

        elif b_type == BusinessProfile.BusinessType.FOP:
            self._validate_required_fields(cleaned_data, [
                ('edrpo', _('ЕДРПО')),
                ('fop_country', _('Страна (деятельности)')),
                ('fop_region', _('Область (деятельности)')),
                ('fop_city', _('Город (деятельности)'))
            ])

            f_country = cleaned_data.get('fop_country')
            f_region = cleaned_data.get('fop_region')
            if f_country and f_region and f_region.country_id != f_country.pk:
                self.add_error('fop_region',
                               _("Область (деятельности) поле: Выбранная область не принадлежит указанной стране."))

        return cleaned_data

    def _validate_required_fields(self, cleaned_data, fields_with_labels):
        for field_name, label in fields_with_labels:
            if not cleaned_data.get(field_name):
                # Тут використовуємо іменований плейсхолдер для гнучкого перекладу
                msg = _("%(label)s поле обязательное для заполнения.") % {'label': label}
                self.add_error(field_name, msg)


class CustomerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("E-Mail*")}),
        label=_("E-Mail"),
        error_messages={
            "required": _("E-Mail поле обязательное для заполнения."),
            "invalid": _("E-Mail не валидний.")
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": _("Пароль*")
        }),
        label=_("Пароль"),
        error_messages={
            "required": _("Пароль поле обязательное для заполнения.")
        }
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError:
            raise ValidationError(
                _("Ваш пароль не соответствует требованиям безопасности."))
        return password


class CustomerForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("E-Mail*")}),
        label=_("E-Mail"),
        error_messages={
            "required": _("E-Mail поле обязательное для заполнения."),
            "invalid": _("E-Mail не валидний.")
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            user = User.objects.get(
                email=email,
                is_active=True,
                is_staff=False,
                is_superuser=False
            )

            if not hasattr(user, 'customer_profile'):
                raise ValidationError(_("У пользователя нет личного кабинета."))
        except User.DoesNotExist:
            raise ValidationError(_("Пользователь с данным E-Mail не обнаружен."))

        return email


class CustomerResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": _("Пароль*")
        }),
        label=_("Пароль"),
        error_messages={
            "required": _("Пароль поле обязательное для заполнения.")
        }
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": _("Подтвердите пароль*")
        }),
        label=_("Подтвердите пароль"),
        error_messages={
            "required": _("Подтвердите пароль поле обязательное для заполнения.")
        }
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError:
            raise ValidationError(
                _("Ваш пароль не соответствует требованиям безопасности."))
        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if all([password, password_confirm]) and password != password_confirm:
            raise ValidationError(_("Пароли не совпадают."))

        return cleaned_data