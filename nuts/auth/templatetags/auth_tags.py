from django import template

from auth.models import (
    RegisterPage,
    LoginPage
)

from profiles.models import ProfilePage

register = template.Library()


@register.inclusion_tag('tags/auth_links.html', takes_context=True)
def auth_links(context):
    return {
        'request': context.get('request'),
        'register_page': RegisterPage.objects.live().first(),
        'login_page': LoginPage.objects.live().first(),
        'profile_page': ProfilePage.objects.live().first(),
    }
