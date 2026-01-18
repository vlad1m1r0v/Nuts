import re
from django import template
from django.utils.safestring import mark_safe

from shop.models import ShopPage
from about.models import AboutPage
from payment_and_delivery.models import PaymentAndDeliveryPage
from customers.models import CustomersPage
from news.models import NewsIndexPage

register = template.Library()


@register.filter
def split_words_br(value):
    if not value:
        return ""

    words = value.upper().split()
    return mark_safe("<br>".join(words))


@register.filter
def clean_phone(value):
    if not value:
        return ""

    return re.sub(r'[^\d+]', '', value)


@register.filter
def format_phone_html(value):
    if not value:
        return ""

    match = re.match(r'^(\+38\s\(0\d{2}\))\s(\d{3}-\d{2}-\d{2})$', value)

    if match:
        prefix = match.group(1)
        rest = match.group(2)
        return mark_safe(f"<span>{prefix}</span> {rest}")

    return value


@register.inclusion_tag('tags/menu_links.html', takes_context=True)
def menu_links(context):
    return {
        'shop_page': ShopPage.objects.live().first(),
        'about_page': AboutPage.objects.live().first(),
        'delivery_page': PaymentAndDeliveryPage.objects.live().first(),
        'customers_page': CustomersPage.objects.live().first(),
        'news_page': NewsIndexPage.objects.live().first(),
        'request': context.get('request')
    }


@register.inclusion_tag('tags/language_switcher.html', takes_context=True)
def language_switcher(context):
    request = context.get('request')
    page = context.get('page') or context.get('self')

    query_parameters = request.GET.urlencode()

    return {
        'request': request,
        'page': page,
        'query_parameters': query_parameters
    }


@register.inclusion_tag('tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self') or context.get('page')

    if self is None:
        return {'ancestors': None}

    ancestors = self.get_ancestors(inclusive=True).filter(depth__gte=2)

    return {
        'ancestors': ancestors,
        'request': context.get('request'),
    }
