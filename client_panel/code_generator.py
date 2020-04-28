import random
from django import template

register = template.Library()


@register.simple_tag
def random_string():
    return str(random.randint(10000, 99999))