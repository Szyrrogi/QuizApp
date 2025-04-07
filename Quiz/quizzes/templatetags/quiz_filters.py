from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.filter(name='string_to_int')
def string_to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0