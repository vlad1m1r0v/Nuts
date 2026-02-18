from django.contrib import messages
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext as _

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from .blocks import ProductImageWithTextBlock


class ProductPage(Page):
    parent_page_types = ['shop.ShopPage']
    subpage_types = []
    max_count = 1

    template = "product.html"

    storage_conditions = models.TextField(blank=True, null=True)

    description_info = StreamField(
        [('image_with_text', ProductImageWithTextBlock())],
        use_json_field=True, max_num=1, blank=True, null=True,
    )

    packaging_info = StreamField(
        [('image_with_text', ProductImageWithTextBlock())],
        use_json_field=True, max_num=1, blank=True, null=True,
    )

    payment_info = StreamField(
        [('image_with_text', ProductImageWithTextBlock())],
        use_json_field=True, max_num=1, blank=True, null=True,
    )

    delivery_info = StreamField(
        [('image_with_text', ProductImageWithTextBlock())],
        use_json_field=True, max_num=1, blank=True, null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("storage_conditions"),
        FieldPanel("description_info"),
        FieldPanel("packaging_info"),
        FieldPanel("payment_info"),
        FieldPanel("delivery_info")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        product_id = request.GET.get('product_id')

        if not product_id:
            messages.error(request, _("Не указан идентфикатор товара."))
            return context

        try:
            product = Product.objects.prefetch_related('images', 'features').get(pk=product_id)
            context['product'] = product
            return context

        except Product.DoesNotExist:
            messages.error(request, _("Товар с указаным идентификатором не обнаружен."))
            return context

    class Meta:
        verbose_name = "Product page"


class ProductFeature(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=64,
        verbose_name="Название особенности"
    )

    class Meta:
        verbose_name = "Особенность товара"
        verbose_name_plural = "Особенности товаров"

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=120,
        verbose_name="Название товара"
    )
    sku = models.CharField(
        max_length=24,
        unique=True,
        verbose_name="Артикул (SKU)"
    )
    weight = models.PositiveIntegerField(
        validators=[
            MinValueValidator(10),
            MaxValueValidator(1000)
        ],
        verbose_name="Вес (г)"
    )
    calories = models.PositiveIntegerField(
        verbose_name="Калорийность (на 100г)"
    )
    shelf_life_months = models.PositiveSmallIntegerField(
        verbose_name="Срок годности (мес.)"
    )
    ingredients = models.TextField(
        verbose_name="Состав"
    )
    features = models.ManyToManyField(
        ProductFeature,
        blank=True,
        verbose_name="Особенности"
    )
    is_new = models.BooleanField(
        default=False,
        verbose_name="Новинка"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Цена со скидкой"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Товар"
    )
    image = models.ImageField(
        upload_to='product_images/',
        verbose_name="Изображение"
    )

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"