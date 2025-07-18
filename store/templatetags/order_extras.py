# store/templatetags/order_extras.py

from django import template

register = template.Library()

@register.filter
def status_choices_up_to(current_status):
    status_list = ['Ordered', 'Processing', 'Out for Delivery', 'Delivered']
    if current_status not in status_list:
        return []
    index = status_list.index(current_status)
    return status_list[:index + 1]