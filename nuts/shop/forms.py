from django import forms

from products.models import ProductFeature

class ProductFilterForm(forms.Form):
    feature = forms.ModelChoiceField(
        queryset=ProductFeature.objects.all(),
        empty_label="Вкус",
        required=False,
    )

    WEIGHT_CHOICES = [
        ('', 'Масса'),
        ('0-50', 'от 0 до 50 г'),
        ('50-100', 'от 50 до 100 г'),
        ('100-200', 'от 100 до 200 г'),
        ('200-400', 'от 200 до 400 г'),
        ('400-9999', 'от 400 г'),
    ]
    weight_range = forms.ChoiceField(
        choices=WEIGHT_CHOICES,
        required=False
    )


    sort_price = forms.ChoiceField(
        choices=[('asc', 'Ascending'), ('desc', 'Descending')],
        required=False,
        widget=forms.HiddenInput()
    )