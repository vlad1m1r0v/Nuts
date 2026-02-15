from cart.models import Cart

def merge_carts(customer_profile, anonymous_session_key):
    if not anonymous_session_key:
        return

    anonymous_cart = Cart.objects.filter(
        session_key=anonymous_session_key,
        is_active=True
    ).first()

    if anonymous_cart:
        anonymous_cart.customer = customer_profile
        anonymous_cart.session_key = None
        anonymous_cart.save()