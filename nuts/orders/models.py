from django.db import models
from core.validators import ukrainian_phone_validator

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'NEW', 'Новый'
        PAID = 'PAID', 'Оплачен'
        PROCESSING = 'PROCESSING', 'В обработке'
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
    status = models.CharField(
        'Статус',
        max_length=10,
        choices=OrderStatus,
        default=OrderStatus.NEW
    )
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
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ №{self.id}"


class OrderContactInformation(models.Model):
    class CustomerType(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', 'Физическое лицо'
        LEGAL = 'LEGAL', 'Юридическое лицо'

    id = models.BigAutoField(primary_key=True)
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='contact_information',
        verbose_name='Заказ'
    )
    email = models.EmailField('Email')
    phone = models.CharField(unique=True, verbose_name="Номер телефона", validators=[ukrainian_phone_validator])
    company_name = models.CharField('Название компании', max_length=255, null=True, blank=True)
    contact_person = models.CharField('Контактное лицо', max_length=255, null=True, blank=True)
    full_name = models.CharField('ФИО', max_length=255, null=True, blank=True)
    customer_type = models.CharField(
        'Тип покупателя',
        max_length=10,
        choices=CustomerType
    )

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'


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