from django.urls import path

from shop.views import ShopCatalogView

app_name = 'shop'

urlpatterns = [
    path(
        route="catalog/",
        view=ShopCatalogView.as_view(),
        name="catalog"
    )
]