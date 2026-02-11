from cart.models import Cart


def cart_processor(request):
    cart = Cart.objects.get_cart_with_totals(request)

    return {
        'cart': cart
    }