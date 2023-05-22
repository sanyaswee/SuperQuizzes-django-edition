from django import template


register = template.Library()


@register.filter
def is_form(model):
    return model.filter(is_form=True)


@register.filter
def is_quiz(model):
    return model.exclude(is_form=True)
