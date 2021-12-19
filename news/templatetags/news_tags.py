from django import template
from datetime import datetime


register = template.Library()


@register.filter
def toDate(value):
    """Removes all values of arg from the given string"""
    return datetime.utcfromtimestamp(value)