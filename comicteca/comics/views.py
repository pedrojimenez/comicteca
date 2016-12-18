"""Comic App views."""

from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse_lazy

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher
from comics.models import Comic
from comics.models import Profile
from comics.models import Saga, ComicsInSaga
# from comics.forms import ArtistCreateForm, ArtistUpdateForm
from comics.forms import ArtistCreateForm
from comics.forms import ColectionCreateForm, ColectionUpdateForm
from comics.forms import CollectionAddComicsForm
from comics.forms import PublisherForm
from comics.forms import ComicForm
from comics.forms import LoginForm
from comics.forms import UserEditForm
from comics.forms import ProfileEditForm


# ------------------------------------------------------------------ #
#
#                        Main view --> index
#
# ------------------------------------------------------------------ #
@login_required
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
@login_required
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


@login_required
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
    """CBV for deleting an Artist model."""

    model = Artist
    success_url = reverse_lazy('artist_list')
    template_name = "comics/delete_artist_confirm.html"


# ------------------------------------------------------------------ #
#
#                         Colection Views
#
# ------------------------------------------------------------------ #
class ColectionCreate(CreateView):
    """CBV for creating a new Collection."""

    def get_form_kwargs(self, **kwargs):
        """Override method for inyecting request.user to form."""
        kwargs = super(ColectionCreate, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs

    model = Colection
    form_class = ColectionCreateForm
    template_name = "comics/add_colection.html"
    # form.fields['current_user'].queryset = request.user
    # success_url = reverse_lazy('colection_list')
    # If form_class is defined fields can not
    # fields = ['name', 'subname', 'volume', 'max_numbers', 'language',
    #           'pub_date', 'distributor', 'editors']


class ColectionUpdate(UpdateView):
    """CBV for updating a Collection."""

    def get_form_kwargs(self, **kwargs):
        """Override method for inyecting request.user to form."""
        kwargs = super(ColectionUpdate, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs

    model = Colection
    form_class = ColectionUpdateForm
    template_name = "comics/update_colection_form.html"
    # fields = ['name', 'subname', 'volume', 'max_numbers', 'language',
    #          'pub_date', 'distributor', 'editors', 'colection_type']


class ColectionDelete(DeleteView):
    """CBV for deleting a Collection."""

    model = Colection
    success_url = reverse_lazy('colection_list')
    template_name = "comics/delete_colection_confirm.html"


class ColectionListView(ListView):
    """CBV for listing all Colection objects."""

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


class CollectionAddComics(UpdateView):
    """CBV for adding Comics to a collection object."""

    def get_form_kwargs(self, **kwargs):
        """Override method for inyecting additional parameters to form."""
        kwargs = super(CollectionAddComics, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        kwargs.update({'current_collection': kwargs['instance']})
        return kwargs

    model = Colection
    template_name = "comics/collection_add_comics.html"
    form_class = CollectionAddComicsForm


@login_required
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


@login_required
def add_colection(request):
    """."""
    if request.method == 'POST':
        form = ColectionCreateForm(request.POST)

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
        form = ColectionCreateForm()
    return render(request, 'comics/add_colection.html', {'form': form})


# ------------------------------------------------------------------ #
#
#                         Publisher Views
#
# ------------------------------------------------------------------ #
@login_required
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


@login_required
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
    """CBV for listing all Publisher objects."""

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
    """CBV for creating an Artist object."""

    model = Publisher
    form_class = PublisherForm
    template_name = "comics/add_publisher.html"
    # success_url = reverse_lazy('publisher_list')
    # fields = ['name', 'history', 'start_date', 'end_date']


class PublisherUpdate(UpdateView):
    """CBV for updating an Artist object."""

    model = Publisher
    form_class = PublisherForm
    template_name = "comics/update_publisher_form.html"
    # fields = ['name', 'history', 'start_date', 'end_date']


class PublisherDelete(DeleteView):
    """CBV for deleting an Artist model."""

    model = Publisher
    success_url = reverse_lazy('publisher_list')
    template_name = "comics/delete_publisher_confirm.html"


# ------------------------------------------------------------------ #
#
#                         Comic Views
#
# ------------------------------------------------------------------ #
@login_required
def comic(request, comic_name_slug):
    """Detailed view for a single comic."""
    context_dict = {}
    try:
        comic = Comic.objects.get(slug=comic_name_slug)

        colection = Colection.objects.get(id=comic.colection.id)
        context_dict['comic'] = comic
        context_dict['colection'] = colection
        context_dict['request_user'] = request.user
        context_dict['inmycollection'] = comic.check_user(request.user)

    except Comic.DoesNotExist:
        # We get here if we didn't find the specified Comic
        # Don't do anything - the template displays the "no comic"
        # message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'comics/comic.html', context_dict)


@login_required
def comic_add_user(request, comic_slug, usr_name):
    """Generic View for adding a comic to user collection."""
    context_dict = {}
    try:
        comic = Comic.objects.get(slug=comic_slug)
        user = User.objects.get(username=usr_name)

        if user not in comic.users.all():
            comic.users.add(user)
        else:
            # TODO: pass it to messages and/or logger
            print "ERROR: User {} already own this comic: {}".format(
                user, comic)

        colection = Colection.objects.get(id=comic.colection.id)
        context_dict['comic'] = comic
        context_dict['colection'] = colection
        context_dict['request_user'] = request.user
        context_dict['inmycollection'] = comic.check_user(request.user)

    except Comic.DoesNotExist:
        # We get here if we didn't find the specified Comic
        # Don't do anything - the template displays the "no comic"
        # message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'comics/comic.html', context_dict)


@login_required
def comic_remove_user(request, comic_slug, usr_name):
    """Generic View for removing a comic to user collection."""
    context_dict = {}
    try:
        comic = Comic.objects.get(slug=comic_slug)
        user = User.objects.get(username=usr_name)

        if user in comic.users.all():
            comic.users.remove(user)
        else:
            # TODO: pass it to messages and/or logger
            print "ERROR: User {} does NOT own this comic: {}".format(
                user, comic)

        colection = Colection.objects.get(id=comic.colection.id)
        context_dict['comic'] = comic
        context_dict['colection'] = colection
        context_dict['request_user'] = request.user
        context_dict['inmycollection'] = comic.check_user(request.user)

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
        # context['object_list'] = Comic.objects.order_by('slug')
        context['total_comics'] = Comic.objects.count()

        return context


class ComicListByUserView(ListView):
    """Generic class view for all Comics from a given User ."""

    model = Comic
    template_name = "comics/comic_list.html"

    def get_context_data(self, **kwargs):
        """Overwriting of method to pass additional info to the template."""
        # Call the base implementation first to get a context
        context = super(ComicListByUserView, self).get_context_data(**kwargs)

        # Add in a QuerySet of all user Comics ordered by inserted date
        context['object_list'] = Comic.objects.filter(
            users__username=self.kwargs['user_slug'])
        context['total_comics'] = context['object_list'].count()
        return context


class ComicCreate(CreateView):
    """CBV for creating a Comic object."""

    model = Comic
    template_name = "comics/add_comic.html"
    form_class = ComicForm
    # fields = ['number', 'colection', 'pages', 'title', 'extrainfo']
    success_url = reverse_lazy('comic_list')


class ComicUpdate(UpdateView):
    """CBV for updating a Comic object."""

    model = Comic
    template_name = "comics/update_comic_form.html"
    form_class = ComicForm
    # fields = ['title', 'number', 'pages', 'extrainfo']


class ComicDelete(DeleteView):
    """CBV for deleting a Artist object."""

    model = Comic
    success_url = reverse_lazy('comic_list')
    template_name = "comics/delete_comic_confirm.html"


# ------------------------------------------------------------------ #
#
#                           Util Views
#
# ------------------------------------------------------------------ #
@login_required
def about(request):
    """About page."""
    return render(request, 'comics/about.html')


# ------------------------------------------------------------------ #
#
#                          Login / Logout
#
# ------------------------------------------------------------------ #
def user_login(request):
    """Default login view."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    real_user = User.objects.get(username=user)
                    if not real_user.profile:
                        Profile.objects.create(user=real_user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    # return render(request, 'registration/login.html', {'form': form})
    return render(request, 'comics/login.html', {'form': form})


# ------------------------------------------------------------------ #
#
#                              Profile
#
# ------------------------------------------------------------------ #
@login_required
def profile_edit(request):
    """Profile edit view."""
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST)

        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,
                             'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request, 'profiles/edit.html',
        {'user_form': user_form, 'profile_form': profile_form})


# ------------------------------------------------------------------ #
#
#                            Saga Views
#
# ------------------------------------------------------------------ #
class SagaListView(ListView):
    """CBV for listing all Saga objects."""

    model = Saga
    template_name = "comics/saga_list.html"

    def get_context_data(self, **kwargs):
        """Overwriting of method to pass additional info to the template."""
        # Call the base implementation first to get a context
        context = super(SagaListView, self).get_context_data(**kwargs)

        # Add in a QuerySet of all the Sagas
        context['object_list'] = Saga.objects.all()

        # TODO: count of money for each saga ==> Annotate this count
        return context


@login_required
def saga(request, saga_slug):
    """."""
    context_dict = {}
    try:
        s = Saga.objects.get(slug=saga_slug)
        saga_comics = ComicsInSaga.objects.filter(saga=s.id).order_by(
            'number_in_saga')

        comic_tuple_list = []
        for saga in saga_comics:
            c = Comic.objects.get(id=saga.comic.id)
            tup = (c, saga.number_in_saga)
            comic_tuple_list.append(tup)

        # Output Example:
        # Comic List Tuple:  [
        # (<Comic: los-vengadores-forum-v1-n1>, 1),
        # (<Comic: los-vengadores-forum-v1-n2>, 2),
        # (<Comic: los-vengadores-forum-v1-n3>, 12)]

        context_dict['comic_list'] = comic_tuple_list
        context_dict['saga'] = s
    except Saga.DoesNotExist:
        # We get here if we didn't find the specified Saga
        # Don't do anything - the template displays the "no saga"
        # message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'comics/saga.html', context_dict)
