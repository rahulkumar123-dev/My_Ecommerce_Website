from django import template
register = template.Library()

@register.filter
def get_item(cart, key):
    return cart.get(str(key), 0)
