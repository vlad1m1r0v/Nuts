from django.db import models
from django.core.validators import MinValueValidator

from wagtail.models import Page

from cart.managers import CartManager

class CartPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['orders.OrderCheckoutPage']
    max_count = 1

    template="cart.html"

    class Meta:
        verbose_name = "Cart page"


class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    customer = models.ForeignKey('users.CustomerProfile', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CartManager()


class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
