# encoding: utf8


from django import template


register = template.Library()


@register.filter
def get_value(form, field):
    return form[field].value()
