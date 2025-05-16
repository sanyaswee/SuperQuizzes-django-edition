from django import template

register = template.Library()

@register.filter
def field(form, name):
    return form[name]
