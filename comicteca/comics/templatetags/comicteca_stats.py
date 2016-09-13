from django import template
from ..models import Colection, Comic, Publisher, Artist

register = template.Library()


@register.simple_tag
def total_colections():
    return Colection.objects.all().count()


@register.simple_tag
def total_comics():
    return Comic.objects.all().count()


@register.simple_tag
def total_publishers():
    return Publisher.objects.all().count()


@register.simple_tag
def total_artists():
    return Artist.objects.all().count()
