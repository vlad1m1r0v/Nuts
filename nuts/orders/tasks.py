import random
from celery import shared_task
from django.db import transaction
from django.db.models import Sum, F
from orders.models import Order
from payment_transactions.models import PaymentTransaction


@shared_task
def simulate_order_processing():
    with transaction.atomic():
        # Використовуємо select_for_update(), щоб уникнути конфліктів при паралельних запусках

        # 5. SHIPPED -> COMPLETED або CANCELED
        # (Обробляємо спочатку "найстаріші" статуси, щоб замовлення не пролітало все за раз)
        shipped_orders = Order.objects.filter(status=Order.OrderStatus.SHIPPED)
        for order in shipped_orders:
            order.status = Order.OrderStatus.COMPLETED if random.random() < 2 / 3 else Order.OrderStatus.CANCELED
            order.save()

        # 4. PAID -> SHIPPED
        paid_orders = Order.objects.filter(status=Order.OrderStatus.PAID)
        for order in paid_orders:
            order.status = Order.OrderStatus.SHIPPED
            order.save()

        # 3. Processing Transaction -> SUCCESSFUL/FAILED (і оновлення Order)
        proc_txs = PaymentTransaction.objects.filter(
            status=PaymentTransaction.TransactionStatus.PROCESSING).select_related('order')
        for tx in proc_txs:
            if random.random() < 2 / 3:
                tx.status = PaymentTransaction.TransactionStatus.SUCCESSFUL
                tx.order.status = Order.OrderStatus.PAID
            else:
                tx.status = PaymentTransaction.TransactionStatus.FAILED
                tx.order.status = Order.OrderStatus.FAILED
            tx.save()
            tx.order.save()

        # 2. NEW Transaction -> PROCESSING (і замовлення теж)
        new_txs = PaymentTransaction.objects.filter(status=PaymentTransaction.TransactionStatus.NEW).select_related(
            'order')
        for tx in new_txs:
            tx.status = PaymentTransaction.TransactionStatus.PROCESSING
            tx.order.status = Order.OrderStatus.PROCESSING
            tx.save()
            tx.order.save()

        # 1. NEW Order -> Create NEW Transaction
        # Тут замовлення ЛИШАЄТЬСЯ в статусі NEW, воно перейде в PROCESSING тільки на наступному кроці/виклику
        new_orders = Order.objects.filter(status=Order.OrderStatus.NEW).exclude(payment_transaction__isnull=False)
        for order in new_orders:
            total_amount = order.items.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0
            PaymentTransaction.objects.create(
                order=order,
                amount=total_amount,
                status=PaymentTransaction.TransactionStatus.NEW
            )