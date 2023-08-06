import json

from django import template

register = template.Library()


@register.filter(name='parseid')
def parseid(value):
    return int(value)
