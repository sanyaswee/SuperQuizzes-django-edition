import random
from django import template
register = template.Library()


@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp


def randcolor():
    return random.randint(0, 255)
