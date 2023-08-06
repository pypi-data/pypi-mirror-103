from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter_function
def js_literal(value):
    js_literal_value = 'null'
    if value is not None:
        if isinstance(value, str):
            js_literal_value = f'"{value}"'
        else:
            js_literal_value = value
    return js_literal_value
