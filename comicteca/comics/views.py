"""Comic App views."""

from django.shortcuts import render
from comics.models import Artist


def index(request):
    """Index view."""

    artists_list = Artist.objects.order_by('-name')[:5]
    context_dict = {'artists': artists_list}

    # Render the response and send it back!
    return render(request, 'comics/index.html', context_dict)
