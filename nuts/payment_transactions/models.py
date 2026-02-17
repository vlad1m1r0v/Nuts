from django.db import models
from orders.models import Order


class PaymentTransaction(models.Model):
    class TransactionStatus(models.TextChoices):
        NEW = 'NEW', 'Новая'
        PROCESSING = 'PROCESSING','В обработке'
        SUCCESSFUL = 'SUCCESSFUL', 'Успешно'
        FAILED = 'FAILED', 'Ошибка'

    id = models.BigAutoField(primary_key=True)

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment_transaction',
        verbose_name='Заказ'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма транзакции'
    )

    status = models.CharField(
        max_length=15,
        choices=TransactionStatus,
        default=TransactionStatus.NEW,
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']