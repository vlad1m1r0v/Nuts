from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from orders.models import Order, OrderItem

from core.validators import ukrainian_phone_validator

from locations.models import Country, Region


class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.customer_profile = kwargs.pop('customer_profile', None)
        super().__init__(*args, **kwargs)

        if not self.initial.get('delivery_method'):
            self.fields['delivery_method'].initial = Order.DeliveryMethod.NOVA_POSHTA

        if not self.initial.get('payment_method'):
            self.fields['payment_method'].initial = Order.PaymentMethod.LIQPAY

        if self.customer_profile:
            self.fields['full_name'].initial = self.customer_profile.full_name
            self.fields['email'].initial = self.customer_profile.user.email
            self.fields['phone'].initial = self.customer_profile.phone

            if hasattr(self.customer_profile, 'business_profile'):
                self.fields['company_name'].initial = self.customer_profile.company_name
                self.fields['contact_person'].initial = self.customer_profile.full_name

    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _("Название компании*")}),
        label=_("Название компании*"),
        min_length=3,
        max_length=255,
        error_messages={
            "max_length": _("Название компанни поле может местить максимум 255 символов."),
            "min_length": _("Название компанни должно местить минимум 3 символа.")
        }
    )

    contact_person = forms.CharField(
        required=False,
        label=_("Контактное лицо*"),
        min_length=3,
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": _("Контактное лицо*")}),
        error_messages={
            "max_length": _("Контактное лицо поле может местить максимум 255 символов."),
            "min_length": _("Контактное лицо должно местить минимум 3 символа.")
        }
    )

    full_name = forms.CharField(
        required=False,
        label=_("ФИО*"),
        min_length=3,
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": _("ФИО*")}),
        error_messages={
            "max_length": _("ФИО поле может местить максимум 255 символов."),
            "min_length": _("ФИО должно местить минимум 3 символа.")
        }
    )

    email = forms.EmailField(
        required=True,
        label=_("E-Mail*"),
        widget=forms.EmailInput(attrs={"placeholder": _("E-Mail*")}),
        error_messages={
            "required": _("Поле E-Mail обязательно для заполнени."),
            "invalid": _("Введите корректный адрес электронной почты.")
        }
    )

    phone = forms.CharField(
        required=True,
        label=_("Номер телефона*"),
        validators=[ukrainian_phone_validator],
        widget=forms.TextInput(attrs={"placeholder": _("Номер телефона*")}),
        error_messages={
            "required": _("Номер телефона обязателен для заполнения."),
        }
    )

    delivery_method = forms.ChoiceField(
        choices=Order.DeliveryMethod,
        label=_("Способ доставки"),
        widget=forms.RadioSelect(),
        error_messages={
            "required": _("Выберите способ доставки."),
            "invalid_choice": _("Выбран недопустимый способ доставки.")
        }
    )

    delivery_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label=_("Страна доставки"),
        empty_label=_("Выберите страну"),
        error_messages={
            "invalid_choice": _("Выбранная страна не существует в базе данных.")
        }
    )

    delivery_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Регион доставки"),
        empty_label=_("Выберите область"),
        error_messages={
            "invalid_choice": _("Выбранная область не существует в базе данных.")
        }
    )

    delivery_address = forms.CharField(
        required=False,
        label=_("Адрес доставки"),
        widget=forms.TextInput(attrs={"placeholder": _("Адрес*")}),
        error_messages={
            "max_length": _("Адрес доставки слишком длинный.")
        }
    )

    payment_method = forms.ChoiceField(
        choices=Order.PaymentMethod,
        label=_("Способ оплаты"),
        widget=forms.RadioSelect(),
        error_messages={
            "required": _("Выберите способ оплаты."),
            "invalid_choice": _("Выбран недопустимый способ оплаты.")
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get('delivery_method')

        is_business = False
        if self.customer_profile and hasattr(self.customer_profile, 'business_profile'):
            is_business = True

        if is_business:
            if not cleaned_data.get('company_name'):
                self.add_error('company_name', _("Название компании обязательно для бизнес-аккаунтов."))
            if not cleaned_data.get('contact_person'):
                self.add_error('contact_person', _("Контактное лицо обязательно для бизнес-аккаунтов."))
        else:
            if not cleaned_data.get('full_name'):
                self.add_error('full_name', _("ФИО обязательно для физических лиц."))

        if delivery_method == Order.DeliveryMethod.NOVA_POSHTA:
            if not cleaned_data.get('delivery_country'):
                self.add_error('delivery_country', _("Выберите страну для доставки Новой Почтой."))
            if not cleaned_data.get('delivery_region'):
                self.add_error('delivery_region', _("Выберите область для доставки Новой Почтой."))

        elif delivery_method == Order.DeliveryMethod.COURIER:
            if not cleaned_data.get('delivery_address'):
                self.add_error('delivery_address', _("Укажите адрес для курьерской доставки по Одессе."))

        country = cleaned_data.get('delivery_country')
        region = cleaned_data.get('delivery_region')
        if country and region and region.country_id != country.pk:
            self.add_error('delivery_region', _("Выбранная область не принадлежит указанной стране."))

        # Clean redundant fields
        if delivery_method == Order.DeliveryMethod.NOVA_POSHTA:
            cleaned_data['delivery_address'] = ""

        elif delivery_method == Order.DeliveryMethod.COURIER:
            cleaned_data['delivery_country'] = None
            cleaned_data['delivery_region'] = None

        elif delivery_method == Order.DeliveryMethod.PICKUP:
            cleaned_data['delivery_country'] = None
            cleaned_data['delivery_region'] = None
            cleaned_data['delivery_address'] = ""

        is_business = self.customer_profile and hasattr(self.customer_profile, 'business_profile')

        if is_business:
            cleaned_data['full_name'] = ""
        else:
            cleaned_data['company_name'] = ""
            cleaned_data['contact_person'] = ""

        return cleaned_data

    class Meta:
        model = Order
        fields = [
            "company_name",
            "contact_person",
            "full_name",
            "email",
            "phone",
            "payment_method",
            "delivery_method",
            "delivery_country",
            "delivery_region",
            "delivery_address",
        ]


class OrderItemForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.TextInput(attrs={
            'class': 'quantity_input order_item__row__quantity',
            'readonly': 'readonly'
        }),
        error_messages={
            'min_value': _("Количество не может быть меньше 1.")
        }
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        widgets = {
            'product': forms.HiddenInput(),
            'price': forms.HiddenInput(),
        }


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=0,
    can_delete=False,
)