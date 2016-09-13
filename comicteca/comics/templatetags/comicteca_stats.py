from django import template
from ..models import Colection

register = template.Library()


@register.simple_tag
def total_colections():
    return Colection.objects.all().count()
