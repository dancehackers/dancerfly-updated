# encoding: utf8


from django import template


register = template.Library()


@register.filter
def ljust(string, width, fillchar=' '):
    try:
        return string.ljust(width, fillchar)
    except (AttributeError, TypeError):
        return ''
