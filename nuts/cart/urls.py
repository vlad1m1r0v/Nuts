from django.urls import path

from cart.views import CartAddItemView, CartUpdateItemView

app_name = 'cart'

urlpatterns = [
    path('add-item/<int:product_id>/', CartAddItemView.as_view(), name='add-item'),
    path('update-item/<int:item_id>/<str:action>', CartUpdateItemView.as_view(), name='update-item'),
]
