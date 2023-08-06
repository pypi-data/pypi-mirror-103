import json

from django import template

register = template.Library()


@register.filter(name='parseid')
def parseid(value):
    try:
        value = int(value)
    except Exception as e:
        print(e)
    return value
