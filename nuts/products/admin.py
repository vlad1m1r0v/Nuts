from django.contrib import admin

# unregister User and Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)

# unregister Image
from wagtail.images.models import Image
import wagtail.images.admin

admin.site.unregister(Image)

# unregister Document
from wagtail.documents.models import Document
import wagtail.documents.admin

admin.site.unregister(Document)

# unregister Media
from wagtailmedia.models import Media
import wagtailmedia.admin

admin.site.unregister(Media)

# unregister Tag
from taggit.models import Tag
import taggit.admin

admin.site.unregister(Tag)

# register Product
from django.utils.html import format_html
from django.db.models import Case, When, F, DecimalField

from django_filters.constants import EMPTY_VALUES

from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import (
    FieldTextFilter,
    MultipleDropdownFilter,
    RangeNumericFilter,
    RangeNumericListFilter
)

from modeltranslation.admin import TabbedTranslationAdmin

from products.models import Product, ProductFeature, ProductImage


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image",)


class ProductFeaturesFilter(MultipleDropdownFilter):
    title = "Особенности (Поиск по всем выбранным)"
    parameter_name = "features"

    def lookups(self, request, model_admin):
        from products.models import ProductFeature
        return [
            [str(f.id), f.name] for f in ProductFeature.objects.all()
        ]

    def queryset(self, request, queryset):
        feature_ids = request.GET.getlist(self.parameter_name)

        feature_ids = [f_id for f_id in feature_ids if f_id not in EMPTY_VALUES]

        if feature_ids:

            for f_id in feature_ids:
                queryset = queryset.filter(features__id=f_id)

            return queryset.distinct()

        return queryset


class ProductPriceFilter(RangeNumericListFilter):
    title = "Актуальная цена"
    parameter_name = "actual_price_range"

    def queryset(self, request, queryset):
        price_from = request.GET.get(f"{self.parameter_name}_from")
        price_to = request.GET.get(f"{self.parameter_name}_to")

        filters = {}
        if price_from:
            filters["actual_price__gte"] = price_from
        if price_to:
            filters["actual_price__lte"] = price_to

        if filters:
            return queryset.annotate(
                actual_price=Case(
                    When(discounted_price__isnull=False, then=F('discounted_price')),
                    default=F('price'),
                    output_field=DecimalField(),
                )
            ).filter(**filters)

        return queryset

@admin.register(Product)
class ProductModelAdmin(ModelAdmin, TabbedTranslationAdmin):
    inlines = [ProductImageInline]

    show_facets = admin.ShowFacets.NEVER

    sortable_by = ()

    list_display = [
        "display_image",
        "name",
        "sku",
        "display_features",
        "display_price",
        "weight",
        "display_is_new"
    ]

    list_filter_submit = True

    list_filter = [
        ("name", FieldTextFilter),
        ProductFeaturesFilter,
        ProductPriceFilter,
        ("weight", RangeNumericFilter)
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("images", "features")

    @admin.display(description="Фото")
    def display_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;" />',
                first_image.image.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: #eee; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #999; font-size: 10px;">No pic</div>'
        )

    @admin.display(description="Особенности")
    def display_features(self, obj):
        features = obj.features.all()
        return ", ".join([f.name for f in features]) if features else "-"

    @admin.display(description="Актуальная цена", ordering="price")
    def display_price(self, obj):
        if obj.discounted_price:
            return format_html(
                '<span style="color: #10b981; font-weight: bold;">{} ₴</span> '
                '<span style="text-decoration: line-through; color: #9ca3af; font-size: 0.85em;">{} ₴</span>',
                obj.discounted_price, obj.price
            )
        return f"{obj.price} ₴"

    @admin.display(description="Новинка", boolean=False)
    def display_is_new(self, obj):
        if obj.is_new:
            return format_html(
                '<span class="bg-primary-600 text-white px-2 py-1 rounded-md text-xs font-bold uppercase">Новинка</span>'
            )
        return "-"


@admin.register(ProductFeature)
class ProductFeatureModelAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_filter_submit = True

    show_facets = admin.ShowFacets.NEVER

    list_filter = [
        ("name", FieldTextFilter),
    ]
