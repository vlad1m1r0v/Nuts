from cart.models import Cart, CartPage


def cart_processor(request):
    cart = Cart.objects.get_cart_with_totals(request)
    cart_page = CartPage.objects.live().first()


    return {
        'cart': cart,
        'cart_page': cart_page
    }