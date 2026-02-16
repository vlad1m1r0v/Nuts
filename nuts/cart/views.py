from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

from products.models import Product

from cart.models import Cart, CartItem

from shop.models import ShopPage

from auth.models import RegisterPage, LoginPage

from orders.models import OrderCheckoutPage

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

        response = HttpResponse()
        response['HX-Trigger'] = 'cartUpdated'
        return response


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

        response = HttpResponse()
        response['HX-Trigger'] = 'cartUpdated'
        return response


class CartPopupView(View):
    def get(self, request):
        cart = Cart.objects.get_cart_with_totals(request)
        return render(request, "includes/cart/popup_content.html", {"cart": cart})


class CartCounterView(View):
    def get(self, request):
        cart = Cart.objects.get_cart_with_totals(request)
        count = getattr(cart, 'cart_items_count', 0) or 0
        return HttpResponse(str(count))


class CartTableView(View):
    def get(self, request):
        cart = Cart.objects.get_cart_with_totals(request)

        shop_page = ShopPage.objects.live().first()
        login_page = LoginPage.objects.live().first()
        register_page = RegisterPage.objects.live().first()
        checkout_page = OrderCheckoutPage.objects.live().first()

        return render(
            request,
            "includes/cart/table.html",
            {
                "cart": cart,
                "shop_page": shop_page,
                "login_page": login_page,
                "register_page": register_page,
                "checkout_page": checkout_page
            }
        )
