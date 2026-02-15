from django.urls import path

from cart.views import (
    CartAddItemView,
    CartUpdateItemView,
    CartPopupView,
    CartCounterView,
    CartTableView
)

app_name = 'cart'

urlpatterns = [
    path('add-item/<int:product_id>/', CartAddItemView.as_view(), name='add-item'),
    path('update-item/<int:item_id>/<str:action>', CartUpdateItemView.as_view(), name='update-item'),
    path('popup/', CartPopupView.as_view(), name='popup'),
    path('counter/', CartCounterView.as_view(), name='counter'),
    path('table/', CartTableView.as_view(), name='table')
]
