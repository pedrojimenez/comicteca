"""Comic App views."""

from django.shortcuts import render
from comics.models import Artist
from comics.models import Colection
from comics.forms import ArtistForm


def index(request):
    """Index view."""
    artists_list = Artist.objects.order_by('-name')[:5]
    colection_list = Colection.objects.order_by('-name')[:5]
    context_dict = {'artists': artists_list, 'colections': colection_list}

    # Render the response and send it back!
    return render(request, 'comics/index.html', context_dict)


def artist(request, artist_name_slug):
    context_dict = {}
    try:
        artist = Artist.objects.get(slug=artist_name_slug)
        # category = Category.objects.get(slug=category_name_slug)
        context_dict['artist_name'] = artist.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        # pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        # context_dict['pages'] = pages
        # We also add the category object from the database to the
        # context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['artist'] = artist
    except Artist.DoesNotExist:
        # We get here if we didn't find the specified artist.
        # Don't do anything - the template displays the "no category"
        # message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'comics/artist.html', context_dict)


def add_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
    else:
        # If the request was not a POST, display the form to enter details.
        form = ArtistForm()
    return render(request, 'comics/add_artist.html', {'form': form})


def colection(request, colection_name_slug):
    context_dict = {}
    try:
        colection = Colection.objects.get(slug=colection_name_slug)
        context_dict['colection_name'] = colection.name
        context_dict['colection'] = colection
    except Colection.DoesNotExist:
        # We get here if we didn't find the specified Colection
        # Don't do anything - the template displays the "no colection"
        # message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'comics/colection.html', context_dict)
