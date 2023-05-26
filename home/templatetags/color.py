from django import template
from django.conf import settings


register = template.Library()


# settings value
@register.simple_tag
def color_class(score):
    if score <= settings.RED_SCORE_COLOR_BORDER:
        return 'red-box'
    elif score <= settings.YELLOW_SCORE_COLOR_BORDER:
        return 'yellow-box'
    else:
        return 'green-box'
