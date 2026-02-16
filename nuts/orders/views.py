from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction

from cart.models import Cart

from home.models import HomePage

from orders.models import OrderCheckoutPage
from orders.forms import OrderCreateForm, OrderItemFormSet

class OrderCreateView(View):
    def post(self, request):
        checkout_page = OrderCheckoutPage.objects.live().first()
        checkout_page_url = checkout_page.get_url(request)

        home_page = HomePage.objects.live().first()
        home_page_url = home_page.get_url(request)

        cart = Cart.objects.get_cart_with_totals(request)
        profile = getattr(request.user, 'customer_profile', None)

        if not cart or cart.cart_items_count == 0:
            messages.error(request, "Ваша корзина пуста.")
            return redirect(checkout_page_url)

        form = OrderCreateForm(request.POST, customer_profile=profile)
        formset = OrderItemFormSet(request.POST)


        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    if profile:
                        order.customer = profile
                    order.save()

                    items = formset.save(commit=False)
                    for item in items:
                        item.order = order
                        item.save()

                    cart.delete()

                    messages.success(request, f"Заказ успешно оформлен.")
                    return redirect(home_page_url)

            except Exception as e:
                messages.error(request, f"Произошла ошибка при сохранении заказа: {str(e)}")
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

            for f_errors in formset.errors:
                for field, errors in f_errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")

            return redirect(request.META.get('HTTP_REFERER', '/'))