from django import forms
from django.forms import inlineformset_factory

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
        widget=forms.TextInput(),
        label="Название компании*",
        min_length=3,
        max_length=255,
        error_messages={
            "max_length": "Название компанни поле может местить максимум 255 символов.",
            "min_length": "Название компанни должно местить минимум 3 символа."
        }
    )

    contact_person = forms.CharField(
        required=False,
        label="Контактное лицо*",
        min_length=3,
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Контактное лицо (ФИО)"}),
        error_messages={
            "max_length": "Контактное лицо поле может местить максимум 255 символов.",
            "min_length": "Контактное лицо должно местить минимум 3 символа."
        }
    )

    full_name = forms.CharField(
        required=False,
        label="ФИО",
        min_length=3,
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "ФИО*"}),
        error_messages={
            "max_length": "ФИО поле может местить максимум 255 символов.",
            "min_length": "ФИО должно местить минимум 3 символа."
        }
    )

    email = forms.EmailField(
        required=True,
        label="E-Mail",
        widget=forms.EmailInput(attrs={"placeholder": "E-Mail*"}),
        error_messages={
            "required": "Поле E-Mail обязательно для заполнения.",
            "invalid": "Введите корректный адрес электронной почты."
        }
    )

    phone = forms.CharField(
        required=True,
        label="Номер телефона",
        validators=[ukrainian_phone_validator],
        widget=forms.TextInput(attrs={"placeholder": "Номер телефона*"}),
        error_messages={
            "required": "Номер телефона обязателен для заполнения.",
        }
    )

    delivery_method = forms.ChoiceField(
        choices=Order.DeliveryMethod,
        label="Способ доставки",
        widget=forms.RadioSelect(),
        error_messages={
            "required": "Выберите способ доставки.",
            "invalid_choice": "Выбран недопустимый способ доставки."
        }
    )

    delivery_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Страна доставки",
        empty_label="Выберите страну",
        error_messages={
            "invalid_choice": "Выбранная страна не существует в базе данных."
        }
    )

    delivery_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Регион доставки",
        empty_label="Выберите область",
        error_messages={
            "invalid_choice": "Выбранная область не существует в базе данных."
        }
    )

    delivery_address = forms.CharField(
        required=False,
        label="Адрес доставки",
        widget=forms.TextInput(attrs={"placeholder": "Адрес*"}),
        error_messages={
            "max_length": "Адрес доставки слишком длинный."
        }
    )

    payment_method = forms.ChoiceField(
        choices=Order.PaymentMethod,
        label="Способ оплаты",
        widget=forms.RadioSelect(),
        error_messages={
            "required": "Выберите способ оплаты.",
            "invalid_choice": "Выбран недопустимый способ оплаты."
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
                self.add_error('company_name', "Название компании обязательно для бизнес-аккаунтов.")
            if not cleaned_data.get('contact_person'):
                self.add_error('contact_person', "Контактное лицо обязательно для бизнес-аккаунтов.")
        else:
            if not cleaned_data.get('full_name'):
                self.add_error('full_name', "ФИО обязательно для физических лиц.")

        if delivery_method == Order.DeliveryMethod.NOVA_POSHTA:
            if not cleaned_data.get('delivery_country'):
                self.add_error('delivery_country', "Выберите страну для доставки Новой Почтой.")
            if not cleaned_data.get('delivery_region'):
                self.add_error('delivery_region', "Выберите область для доставки Новой Почтой.")

        elif delivery_method == Order.DeliveryMethod.COURIER:
            if not cleaned_data.get('delivery_address'):
                self.add_error('delivery_address', "Укажите адрес для курьерской доставки по Одессе.")

        country = cleaned_data.get('delivery_country')
        region = cleaned_data.get('delivery_region')
        if country and region and region.country_id != country.pk:
            self.add_error('delivery_region', "Выбранная область не принадлежит указанной стране.")

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
            "payment_method"
        ]


class OrderItemForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.TextInput(attrs={
            'class': 'quantity_input order_item__row__quantity',
            'readonly': 'readonly'
        }),
        error_messages={
            'min_value': "Количество не может быть меньше 1."
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