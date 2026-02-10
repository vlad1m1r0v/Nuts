from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Case, When, F, DecimalField
from products.models import Product

from .forms import ProductFilterForm

class ShopCatalogView(View):
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all().prefetch_related('images', 'features')

        form = ProductFilterForm(request.GET)
        if form.is_valid():
            feature = form.cleaned_data.get('feature')

            if feature:
                queryset = queryset.filter(features=feature)

            weight_range = form.cleaned_data.get('weight_range')

            if weight_range:
                try:
                    w_min, w_max = weight_range.split('-')
                    queryset = queryset.filter(weight__gte=w_min, weight__lte=w_max)
                except ValueError:
                    pass

            queryset = queryset.annotate(
                actual_price=Case(
                    When(discounted_price__isnull=False, then=F('discounted_price')),
                    default=F('price'),
                    output_field=DecimalField(),
                )
            )

            sort = form.cleaned_data.get('sort_price')

            if sort == 'asc':
                queryset = queryset.order_by('actual_price')
            elif sort == 'desc':
                queryset = queryset.order_by('-actual_price')

        paginator = Paginator(queryset, 1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'page_obj': page_obj,
            'filter_form': form
        }

        return render(request, "includes/shop/cards.html", context)