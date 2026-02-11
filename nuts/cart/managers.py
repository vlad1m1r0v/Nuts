from django.db import models
from django.db.models import F, Sum, DecimalField, ExpressionWrapper, Case, When

from django.apps import apps


class CartQuerySet(models.QuerySet):
    def with_totals(self):
        CartItem = apps.get_model('cart', 'CartItem')

        return self.prefetch_related(
            models.Prefetch(
                'items',
                queryset=CartItem.objects.annotate(
                    actual_price=Case(
                        When(product__discounted_price__isnull=False, then=F('product__discounted_price')),
                        default=F('product__price'),
                        output_field=DecimalField(),
                    )
                ).annotate(
                    item_total=ExpressionWrapper(
                        F('actual_price') * F('quantity'),
                        output_field=DecimalField()
                    )
                )
            )
        ).annotate(
            cart_total=Sum(
                Case(
                    When(items__product__discounted_price__isnull=False,
                         then=F('items__product__discounted_price') * F('items__quantity')),
                    default=F('items__product__price') * F('items__quantity'),
                    output_field=DecimalField(),
                )
            ),
            cart_items_count=Sum('items__quantity')
        )

    def for_user_or_session(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'customer_profile'):
            return self.filter(customer=request.user.customer_profile, is_active=True)

        session_key = request.session.session_key

        if not session_key:
            return self.none()
        return self.filter(session_key=session_key, is_active=True)


class CartManager(models.Manager):
    def get_queryset(self):
        return CartQuerySet(self.model, using=self._db)

    def get_cart_with_totals(self, request):
        return self.get_queryset().for_user_or_session(request).with_totals().first()