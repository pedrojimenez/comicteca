"""Comic App views."""

from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy

from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher
from comics.forms import ArtistForm
from comics.forms import ColectionForm
from comics.forms import PublisherForm


def index(request):
    """Index view."""
    artists_list = Artist.objects.order_by('-name')[:5]
    colection_list = Colection.objects.order_by('-name')[:5]
    publisher_list = Publisher.objects.order_by('-name')[:5]
    context_dict = {'artists': artists_list, 'colections': colection_list,
                    'publishers': publisher_list}

    # Render the response and send it back!
    return render(request, 'comics/index.html', context_dict)


def artist(request, artist_name_slug):
    """."""
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
    """."""
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the term
            print form.errors

    else:
        # If the request was not a POST, display the form to enter details.
        form = ArtistForm()
    return render(request, 'comics/add_artist.html', {'form': form})


class ArtistListView(ListView):
    """Generic class view for all Artists models."""

    model = Artist
    template_name = "comics/artist_list.html"

    def get_context_data(self, **kwargs):
        """Overwriting of method to pass additional info to the template."""

        # Call the base implementation first to get a context
        context = super(ArtistListView, self).get_context_data(**kwargs)

        # Add in a QuerySet of all the Artists ordered by slug name
        context['artist_list'] = Artist.objects.order_by('slug')

        # TODO: count of comics for each artist ==> Annotate this count
        return context


class ArtistCreate(CreateView):
    """."""

    model = Artist
    template_name = "comics/add_artist.html"
    fields = ['name', 'nationality', 'birthdate', 'deathdate',
              'biography']


class ArtistUpdate(UpdateView):
    """."""

    model = Artist
    template_name = "comics/artist_update_form.html"
    fields = ['name', 'nationality', 'birthdate', 'deathdate',
              'biography']


class ArtistDelete(DeleteView):
    """."""

    model = Artist
    # success_url = reverse_lazy('artist-list')
    success_url = reverse_lazy('index')

# ------------------------------------------------------------------ #
#
#                         Colection Views
#
# ------------------------------------------------------------------ #
class ColectionCreate(CreateView):
    """."""

    model = Colection
    template_name = "comics/add_colection.html"
    success_url = reverse_lazy('index')
    fields = ['name', 'subname', 'volume', 'max_numbers', 'language',
              'pub_date', 'distributors', 'editors']

class ColectionListView(ListView):
    """Generic class view for all Colection models."""

    model = Colection
    template_name = "comics/colection_list.html"

    def get_context_data(self, **kwargs):
        """Overwriting of method to pass additional info to the template."""

        # Call the base implementation first to get a context
        context = super(ColectionListView, self).get_context_data(**kwargs)

        # Add in a QuerySet of all the Artists ordered by slug name
        context['colection_list'] = Colection.objects.order_by('slug')

        # TODO: count of money for each colection ==> Annotate this count
        return context


def colection(request, colection_name_slug):
    """."""
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


def add_colection(request):
    """."""
    if request.method == 'POST':
        form = ColectionForm(request.POST)

        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the term
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = ColectionForm()
    return render(request, 'comics/add_colection.html', {'form': form})


def publisher(request, publisher_name_slug):
    """."""
    context_dict = {}
    try:
        publisher = Publisher.objects.get(slug=publisher_name_slug)
        context_dict['publisher_name'] = publisher.name
        context_dict['publisher'] = publisher
    except Publisher.DoesNotExist:
        # We get here if we didn't find the specified Publisher
        # Don't do anything - the template displays the "no colection"
        # message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'comics/publisher.html', context_dict)


def add_publisher(request):
    """."""
    if request.method == 'POST':
        form = PublisherForm(request.POST)

        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the term
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = PublisherForm()
    return render(request, 'comics/add_publisher.html', {'form': form})


def about(request):
    """."""
    return render(request, 'comics/about.html')
