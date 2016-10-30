"""Comic App views."""

from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse_lazy

from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher
from comics.models import Comic
# from comics.forms import ArtistCreateForm, ArtistUpdateForm
from comics.forms import ArtistCreateForm
from comics.forms import ColectionForm
from comics.forms import PublisherForm
from comics.forms import ComicForm


def index(request):
    """Index view."""
    artists_list = Artist.objects.order_by('-inserted')[:5]
    colection_list = Colection.objects.order_by('-inserted')[:5]
    publisher_list = Publisher.objects.order_by('-inserted')[:5]
    comic_list = Comic.objects.order_by('-inserted')[:5]
    context_dict = {'artists': artists_list, 'colections': colection_list,
                    'publishers': publisher_list, 'comics': comic_list}

    # Render the response and send it back!
    return render(request, 'comics/index.html', context_dict)


# ------------------------------------------------------------------ #
#
#                           Artist Views
#
# ------------------------------------------------------------------ #
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
        form = ArtistCreateForm(request.POST)
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
        form = ArtistCreateForm()
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
    """CBV for creating an Artist model."""

    model = Artist
    form_class = ArtistCreateForm
    template_name = "comics/add_artist.html"
    # fields = ['name', 'nationality', 'birthdate', 'deathdate',
    #           'biography', 'extrainfo', 'image_url']


class ArtistUpdate(UpdateView):
    """CBV for updating an Artist model."""

    model = Artist
    form_class = ArtistCreateForm
    template_name = "comics/update_artist_form.html"
    # fields = ['name', 'nationality', 'birthdate', 'deathdate',
    #           'biography', 'extrainfo', 'image_url']


class ArtistDelete(DeleteView):
    """."""

    model = Artist
    success_url = reverse_lazy('artist_list')
    template_name = "comics/delete_artist_confirm.html"


# ------------------------------------------------------------------ #
#
#                         Colection Views
#
# ------------------------------------------------------------------ #
class ColectionCreate(CreateView):
    """CBV for creating a new object Colection."""

    model = Colection
    form_class = ColectionForm
    template_name = "comics/add_colection.html"
    # success_url = reverse_lazy('colection_list')
    # If form_class is defined fields can not
    # fields = ['name', 'subname', 'volume', 'max_numbers', 'language',
    #           'pub_date', 'distributor', 'editors']


class ColectionUpdate(UpdateView):
    """."""

    model = Colection
    form_class = ColectionForm
    template_name = "comics/update_colection_form.html"
    # fields = ['name', 'subname', 'volume', 'max_numbers', 'language',
    #          'pub_date', 'distributor', 'editors', 'colection_type']


class ColectionDelete(DeleteView):
    """."""

    model = Colection
    success_url = reverse_lazy('colection_list')
    template_name = "comics/delete_colection_confirm.html"


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
        colection_editors = Colection.objects.get(
            slug=colection_name_slug).editors.all().order_by('slug')
        colection_comics = Comic.objects.filter(
            colection__id=colection.id).order_by('number')

        # filter(colection__editors__set)
        context_dict['colection_name'] = colection.name
        context_dict['colection'] = colection
        context_dict['editor_list'] = colection_editors
        context_dict['comic_list'] = colection_comics
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


# ------------------------------------------------------------------ #
#
#                         Publisher Views
#
# ------------------------------------------------------------------ #
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


class PublisherListView(ListView):
    """Generic class view for all Publisher models."""

    model = Publisher
    template_name = "comics/publisher_list.html"

    def get_context_data(self, **kwargs):
        """Overwriting of method to pass additional info to the template."""
        # Call the base implementation first to get a context
        context = super(PublisherListView, self).get_context_data(**kwargs)

        # Add in a QuerySet of all the Artists ordered by slug name
        context['publisher_list'] = Publisher.objects.order_by('slug')

        return context


class PublisherCreate(CreateView):
    """."""

    model = Publisher
    form_class = PublisherForm
    template_name = "comics/add_publisher.html"
    # success_url = reverse_lazy('publisher_list')
    # fields = ['name', 'history', 'start_date', 'end_date']


class PublisherUpdate(UpdateView):
    """."""

    model = Publisher
    form_class = PublisherForm
    template_name = "comics/update_publisher_form.html"
    # fields = ['name', 'history', 'start_date', 'end_date']


class PublisherDelete(DeleteView):
    """."""

    model = Publisher
    success_url = reverse_lazy('publisher_list')
    template_name = "comics/delete_publisher_confirm.html"


# ------------------------------------------------------------------ #
#
#                         Comic Views
#
# ------------------------------------------------------------------ #
def comic(request, comic_name_slug):
    """."""
    context_dict = {}
    try:
        comic = Comic.objects.get(slug=comic_name_slug)

        colection = Colection.objects.get(id=comic.colection.id)
        context_dict['comic'] = comic
        context_dict['colection'] = colection

    except Comic.DoesNotExist:
        # We get here if we didn't find the specified Comic
        # Don't do anything - the template displays the "no comic"
        # message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'comics/comic.html', context_dict)


class ComicDetailView(DetailView):
    """Generic class view for all Comics models of a Colection."""

    model = Comic
    template_name = "comics/comic_detail.html"

    def get_context_data(self, **kwargs):
        """Overwriting of method to pass additional info to the template."""
        # Call the base implementation first to get a context
        context = super(ComicDetailView, self).get_context_data(**kwargs)
        print "entrando en Comic Detail View"
        print self.kwargs
        # Add in a QuerySet of all the Comics ordered by inserted date
        # context['comic_list'] = Comic.objects.order_by('slug')
        # cntext['colection'] = Colection.objects.get(slug=colection_name_slug)

        return context


class ComicListView(ListView):
    """Generic class view for all Comics models of a Colection."""

    model = Comic
    template_name = "comics/comic_list.html"

    def get_context_data(self, **kwargs):
        """Overwriting of method to pass additional info to the template."""
        # Call the base implementation first to get a context
        context = super(ComicListView, self).get_context_data(**kwargs)

        # Add in a QuerySet of all the Comics ordered by inserted date
        # context['comic_list'] = Comic.objects.order_by('slug')
        context['total_comics'] = len(Comic.objects.all())

        return context


class ComicCreate(CreateView):
    """."""

    model = Comic
    template_name = "comics/add_comic.html"
    form_class = ComicForm
    # fields = ['number', 'colection', 'pages', 'title', 'extrainfo']
    success_url = reverse_lazy('comic_list')


class ComicUpdate(UpdateView):
    """."""

    model = Comic
    template_name = "comics/update_comic_form.html"
    form_class = ComicForm
    # fields = ['title', 'number', 'pages', 'extrainfo']


class ComicDelete(DeleteView):
    """."""

    model = Comic
    success_url = reverse_lazy('comic_list')
    template_name = "comics/delete_comic_confirm.html"


# ------------------------------------------------------------------ #
#
#                           Util Views
#
# ------------------------------------------------------------------ #
def about(request):
    """."""
    return render(request, 'comics/about.html')
