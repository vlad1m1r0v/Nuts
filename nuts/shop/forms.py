from django import forms
from django.utils.translation import gettext_lazy as _

from products.models import ProductFeature

class ProductFilterForm(forms.Form):
    feature = forms.ModelChoiceField(
        queryset=ProductFeature.objects.all(),
        empty_label=_("Вкус"),
        required=False,
    )

    WEIGHT_CHOICES = [
        ('', _("Масса")),
        ('0-50', _("от 0 до 50 г")),
        ('50-100', _("от 50 до 100 г")),
        ('100-200', _("от 100 до 200 г")),
        ('200-400', _("от 200 до 400 г")),
        ('400-9999', _("от 400 г")),
    ]
    weight_range = forms.ChoiceField(
        choices=WEIGHT_CHOICES,
        required=False
    )

    sort_price = forms.ChoiceField(
        choices=[
            ('asc', _("По возрастанию")),
            ('desc', _("По убыванию"))
        ],
        required=False,
        widget=forms.HiddenInput()
    )