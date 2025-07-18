from django import template

register = template.Library()

@register.filter
def status_choices_up_to(current_status):
    choices = ['Ordered', 'Processing', 'Out for Delivery', 'Delivered']
    if current_status in choices:
        index = choices.index(current_status)
        return choices[:index + 1]
    return []