from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def urlize_target_blank(value, autoescape=None):
    return value.replace("<a", '<a target="_blank"')
