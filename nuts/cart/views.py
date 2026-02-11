from django.views import View
from django.shortcuts import render

from products.models import Product

from cart.models import Cart, CartItem


class CartAddItemView(View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)

        if request.user.is_authenticated and hasattr(request.user, "customer_profile"):
            cart, _ = Cart.objects.get_or_create(
                customer=request.user.customer_profile,
                is_active=True,
            )
        else:
            if not request.session.session_key:
                request.session.create()
            cart, _ = Cart.objects.get_or_create(
                session_key=request.session.session_key,
                is_active=True
            )

        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})

        if not created:
            item.quantity += 1
            item.save()
        else:
            item.quantity = 1
            item.save()

        updated_cart = Cart.objects.get_cart_with_totals(request)

        is_htmx = request.headers.get('HX-Request') == 'true'

        return render(request, "includes/cart/content.html", {
            "cart": updated_cart,
            "is_htmx": is_htmx
        })


class CartUpdateItemView(View):
    def post(self, request, item_id, action):
        item = CartItem.objects.get(id=item_id)

        if action == 'plus':
            item.quantity += 1
            item.save()

        elif action == 'minus':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

        elif action == 'remove':
            item.delete()

        updated_cart = Cart.objects.get_cart_with_totals(request)
        is_htmx = request.headers.get('HX-Request') == 'true'

        return render(request, "includes/cart/content.html", {
            "cart": updated_cart,
            "is_htmx": is_htmx
        })