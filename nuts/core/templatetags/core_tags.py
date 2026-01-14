import re
from django import template
from django.utils.safestring import mark_safe

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
