from django import template
from django.conf import settings
from home.models import Tag


register = template.Library()


def key(tag: Tag):
    return settings.ALPHABET.find(str(tag.localized_uk_ua)[0].lower())


@register.filter
def sort(arg):
    tmp = list(arg)[:]
    return sorted(tmp, key=key)
