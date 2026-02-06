from django import template

from profiles.models import (
    OrdersHistoryPage,
    TransactionsHistoryPage,
    ContactInformationPage,
    ChangePasswordPage,
    AddressPage
)

register = template.Library()


@register.inclusion_tag('tags/profile_menu_links.html', takes_context=True)
def profile_menu_links(context):
    current_page = context.get('self') or context.get('page')

    return {
        'current_page': current_page,
        'orders_history_page': OrdersHistoryPage.objects.live().first(),
        'transactions_history_page': TransactionsHistoryPage.objects.live().first(),
        'contact_information_page': ContactInformationPage.objects.live().first(),
        'change_password_page': ChangePasswordPage.objects.live().first(),
        'address_page': AddressPage.objects.live().first()
    }