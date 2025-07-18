from django import template
from store.models import Order

register = template.Library()

@register.filter
def status_choices_up_to(current_status):
    choices = [choice[0] for choice in Order.STATUS_CHOICES]
    if current_status in choices:
        index = choices.index(current_status)
        return choices[:index + 1]
    return []