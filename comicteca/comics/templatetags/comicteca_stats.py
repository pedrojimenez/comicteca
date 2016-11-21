from django import template
from ..models import Colection, Comic, Publisher, Artist

register = template.Library()


@register.simple_tag
def total_colections():
    return Colection.objects.count()


@register.simple_tag
def total_comics():
    return Comic.objects.count()


@register.simple_tag
def total_publishers():
    return Publisher.objects.count()


@register.simple_tag
def total_artists():
    return Artist.objects.count()


@register.simple_tag
def total_retail_currency():
    collection_list = Colection.objects.all()
    total_cash = 0
    for collection in collection_list:
        total_cash += collection.get_currency(unit='euros',
                                              output_format='integer')
    return total_cash


@register.simple_tag
def total_paid_currency():
    collection_list = Colection.objects.all()
    total_cash = 0
    for collection in collection_list:
        total_cash += collection.get_paid(unit='euros',
                                          output_format='integer')
    return total_cash
