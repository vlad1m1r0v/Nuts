from django.db import transaction

from cart.models import Cart

def merge_carts(customer_profile, anonymous_session_key):
    if not anonymous_session_key:
        return

    anonymous_cart = Cart.objects.filter(
        session_key=anonymous_session_key,
        is_active=True
    ).first()

    if not anonymous_cart:
        return

    user_cart = Cart.objects.filter(
        customer=customer_profile,
        is_active=True
    ).first()

    with transaction.atomic():
        if not user_cart:
            anonymous_cart.customer = customer_profile
            anonymous_cart.session_key = None
            anonymous_cart.save()
        else:
            anonymous_items = anonymous_cart.items.all()

            for item in anonymous_items:
                existing_item = user_cart.items.filter(product=item.product).first()

                if existing_item:
                    existing_item.quantity += item.quantity
                    existing_item.save()
                    item.delete()
                else:
                    item.cart = user_cart
                    item.save()

            anonymous_cart.delete()