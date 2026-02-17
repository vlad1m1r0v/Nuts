from django.db import models

from wagtail.models import Page

from core.validators import ukrainian_phone_validator
from auth.mixins import CustomerProfileRequiredMixin

from cart.models import Cart


class OrderCheckoutPage(CustomerProfileRequiredMixin, Page):
    parent_page_types = ['cart.CartPage']
    subpage_types = []
    max_count = 1

    template = "checkout.html"

    def get_context(self, request, *args, **kwargs):
        from orders.forms import OrderCreateForm, OrderItemFormSet

        context = super().get_context(request, *args, **kwargs)

        profile = getattr(request.user, 'customer_profile', None)

        cart = Cart.objects.get_cart_with_totals(request)

        form = OrderCreateForm(customer_profile=profile)

        initial_items = [
            {
                'product': item.product,
                'quantity': item.quantity,
                'price': item.actual_price
            }
            for item in cart.items.all()
        ]

        formset = OrderItemFormSet(initial=initial_items)
        formset.extra = len(initial_items)

        context['form'] = form
        context['formset'] = formset
        context['cart'] = cart

        return context

    class Meta:
        verbose_name = "Order checkout page"


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'NEW', 'Новый'
        PROCESSING = 'PROCESSING', 'В обработке'
        PAID = 'PAID', 'Оплачен'
        FAILED = 'FAILED', 'Провален'
        SHIPPED = 'SHIPPED', 'Отправлен'
        COMPLETED = 'COMPLETED', 'Завершен'
        CANCELED = 'CANCELED', 'Отменен'

    class DeliveryMethod(models.TextChoices):
        NOVA_POSHTA = 'NOVA_POSHTA', 'Новая Почта'
        COURIER = 'COURIER', 'Курьер'
        PICKUP = 'PICKUP', 'Самовывоз'

    class PaymentMethod(models.TextChoices):
        LIQPAY = 'LIQPAY', 'Liqpay'
        BANK_TRANSFER = 'BANK_TRANSFER', 'Банковский перевод'
        CASH_ON_DELIVERY = 'CASH_ON_DELIVERY', 'Наложенный платеж'

    id = models.BigAutoField(primary_key=True)

    customer = models.ForeignKey(
        'users.CustomerProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Покупатель'
    )
    # Contacts
    company_name = models.CharField('Название компании', max_length=255, null=True, blank=True)
    contact_person = models.CharField('Контактное лицо', max_length=255, null=True, blank=True)
    full_name = models.CharField('ФИО', max_length=255, null=True, blank=True)
    email = models.EmailField('E-Mail', default="example@domain.com")
    phone = models.CharField(
        unique=True,
        verbose_name="Номер телефона",
        validators=[ukrainian_phone_validator],
        default="+38 (099) 999-99-99"
    )
    # Status
    status = models.CharField(
        'Статус',
        max_length=10,
        choices=OrderStatus,
        default=OrderStatus.NEW
    )
    # Delivery information
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=16,
        choices=PaymentMethod
    )
    delivery_method = models.CharField(
        'Способ доставки',
        max_length=11,
        choices=DeliveryMethod
    )
    delivery_country = models.ForeignKey(
        'locations.Country',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Страна доставки'
    )
    delivery_region = models.ForeignKey(
        'locations.Region',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Регион доставки'
    )
    delivery_address = models.TextField('Адрес доставки', null=True, blank=True)
    # Timestamps
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField('Количество')
    price = models.DecimalField('Цена на момент заказа', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
