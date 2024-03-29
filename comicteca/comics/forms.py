"""Forms for Comic app."""
from django import forms
from django.contrib.auth.models import User

from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher
from comics.models import Comic
from comics.models import Profile
from comics.models import Saga
from comics.models import ComicsInSaga
from comics.models import Ownership
from image_manager.models import ImageManager
from comics.utils import parse_int_set

from django.core.files.base import ContentFile
from django.utils.text import slugify
from django_countries.fields import CountryField


# ------------------------------------------------------------------ #
#
#                           Artist Forms
#
# ------------------------------------------------------------------ #
class ArtistCreateForm(forms.ModelForm):
    """Artist form."""

    image_manager = ImageManager()
    name = forms.CharField(max_length=128, label="Name",
                           help_text="Please enter the Artist name.")
    nationality = CountryField(blank_label='(select country)',
                               help_text="Nationality")
    birthdate = forms.DateField(label="Birth Date", required=False,
                                help_text="Author birth date")
    deathdate = forms.DateField(label="Death Date", required=False,
                                help_text="Author Death date")
    biography = forms.CharField(widget=forms.Textarea, max_length=3000,
                                label="Biography",
                                required=False, help_text="Author Biography")
    extrainfo = forms.URLField(label="Extra Info (URL)",
                               required=False, help_text="Author Extra Info")
    imageurl = forms.URLField(label="Artist Portrait URL", required=False,
                              help_text="Formats: {}".format(
                                  image_manager.valid_extensions))
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        """Meta class for Artist Form."""

        # Provide an association between the ModelForm and a model
        model = Artist
        fields = ('name', 'nationality', 'birthdate', 'deathdate',
                  'biography', 'extrainfo')

    def clean_imageurl(self):
        """Clean method for imageurl form field."""
        url = self.cleaned_data['imageurl']
        if url:
            if not self.image_manager.is_valid_image_extension(url):
                msg = 'The given URL does not match valid image extensions.'
                raise forms.ValidationError(msg)
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """."""
        artist = super(ArtistCreateForm, self).save(commit=False)

        image_url = self.cleaned_data['imageurl']
        # download image from the given URL
        if image_url:
            response = self.image_manager.check_http_url(image_url)
            if response:
                image_type = image_url.rsplit('.', 1)[1].lower()
                image_name = slugify(artist.name) + '.' + image_type
                artist.image.save(image_name, ContentFile(response.read()),
                                  save=False)
        if commit:
            artist.save()
        return artist


# ------------------------------------------------------------------ #
#
#                        Collection Forms
#
# ------------------------------------------------------------------ #
class ColectionCreateForm(forms.ModelForm):
    """Colection form."""

    def __init__(self, *args, **kwargs):
        """Contructor for ColectionForm class."""
        self.request_user = kwargs.pop('current_user')
        # Now kwargs doesn't contain 'current_user' ==>
        # so we can safely pass it to the base class method
        super(ColectionCreateForm, self).__init__(*args, **kwargs)

    image_manager = ImageManager()
    name = forms.CharField(
        max_length=128,
        label="Name",
        help_text="Please enter the Colection name")

    subname = forms.CharField(
        max_length=128,
        label="Name",
        required=False,
        help_text="Please enter the Colection subname")

    volume = forms.IntegerField(
        label="Volume",
        min_value=0,
        initial=1,
        help_text='Volume')

    colection_type = forms.ChoiceField(
        label="Type",
        choices=Colection.TYPE_OF_COLECTION)

    collection_format = forms.ChoiceField(
        label="Format",
        choices=Colection.FORMAT_OF_COLLECTION)

    editors = forms.ModelMultipleChoiceField(
        queryset=Publisher.objects.all(),
        label="Edition Publishers",
        help_text="Editors")

    distributor = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        label="Distribution Publishers",
        help_text="Distributor")

    max_numbers = forms.IntegerField(
        label="Total numbers",
        min_value=1,
        initial=1,
        help_text='Total numbers')

    language = CountryField(
        blank_label='(select country)',
        help_text="Colection Language")

    pub_date = forms.DateField(
        label="Publication Date",
        required=False,
        help_text="Colection publication date")

    imageurl = forms.URLField(
        label="Colection Image URL",
        required=False,
        help_text="Formats: {}".format(image_manager.valid_extensions))

    full_colection = forms.BooleanField(
        label="Add comics",
        required=False,
        help_text="Fill the colection with all comics")

    input_range = forms.CharField(
        max_length=128,
        label="Range",
        required=False,
        help_text="Please enter a valid range")

    pages = forms.IntegerField(
        label="Pages",
        min_value=1,
        initial=24,
        required=False,
        help_text='Number of pages of each comic')

    purchase_price = forms.FloatField(
        label="Purchase Price",
        initial=0,
        required=False,
        help_text='Money paid for these comics')

    purchase_unit = forms.ChoiceField(
        label="currency",
        choices=Comic.CURRENCY_TYPES)

    retail_price = forms.FloatField(
        label="Retail Price",
        initial=0,
        required=False,
        help_text='Real price of each comic')

    retail_unit = forms.ChoiceField(
        label="currency",
        choices=Comic.CURRENCY_TYPES)

    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)

    class Meta:
        """Meta class for Colection Form."""

        # Provide an association between the ModelForm and a model
        model = Colection
        fields = ('name', 'subname', 'volume', 'editors', 'distributor',
                  'max_numbers', 'initial_number', 'language', 'pub_date',)

    def clean_imageurl(self):
        """Clean method for imageurl form field."""
        url = self.cleaned_data['imageurl']
        if url:
            if not self.image_manager.is_valid_image_extension(url):
                msg = 'The given URL does not match valid image extensions.'
                raise forms.ValidationError(msg)
        return url

    def clean_input_range(self):
        """Clean method for input_range form field."""
        my_range = self.cleaned_data['input_range']
        max_numbers = self.cleaned_data['max_numbers']
        if my_range:
            selection, invalid = parse_int_set(inputstr=my_range,
                                               max=max_numbers)
            if invalid:
                # msg = 'Invalid input values: {}'.format(str(invalid))
                msg = 'Invalid input values: {}'.format(
                    ", ".join(str(item) for item in invalid))
                raise forms.ValidationError(msg)
        return my_range

    def save(self, commit=True):
        """Overrride of save method in Colection Form."""
        collection = super(ColectionCreateForm, self).save(commit=False)

        # do custom stuff
        collection.colection_type = self.cleaned_data['colection_type']
        collection.colection_format = self.cleaned_data['collection_format']
        image_url = self.cleaned_data['imageurl']

        # download image from the given URL
        if image_url:
            response = self.image_manager.check_http_url(image_url)
            if response:
                image_type = image_url.rsplit('.', 1)[1].lower()
                image_name = slugify(collection.name) + '_' + \
                    slugify(collection.subname) + '_v' + \
                    str(collection.volume) + '_' + \
                    slugify(collection.distributor) + '.' + image_type
                # Example: daredevil_fall-from-paradise_v1_forum.jpg
                collection.image.save(image_name, ContentFile(response.read()),
                                      save=False)

        if commit:
            collection.save()
            col = Colection.objects.get(
                name=self.cleaned_data['name'],
                volume=self.cleaned_data['volume'],
                distributor=self.cleaned_data['distributor'])
            if col:
                # custom actions once the Colection is saved
                # 1.) Add all related editors
                if self.cleaned_data['editors']:
                    for editor in self.cleaned_data['editors']:
                        col.editors.add(editor)

                # 2.) if full_colection / range  ==> Add all related comics
                if self.cleaned_data['full_colection']:
                    col.complete_colection(
                        user=self.request_user,
                        pages=self.cleaned_data['pages'],
                        retail_price=self.cleaned_data['retail_price'],
                        retail_unit=self.cleaned_data['retail_unit'],
                        purchase_price=self.cleaned_data['purchase_price'],
                        purchase_unit=self.cleaned_data['purchase_unit'])
                elif self.cleaned_data['input_range']:
                    col.complete_colection(
                        user=self.request_user,
                        rangeset=self.cleaned_data['input_range'],
                        pages=self.cleaned_data['pages'],
                        retail_price=self.cleaned_data['retail_price'],
                        retail_unit=self.cleaned_data['retail_unit'],
                        purchase_price=self.cleaned_data['purchase_price'],
                        purchase_unit=self.cleaned_data['purchase_unit'])

                # TODO: refactor previous code to make a single calling
        return collection


class ColectionUpdateForm(forms.ModelForm):
    """Colection Update form."""

    def __init__(self, *args, **kwargs):
        """Contructor for ColectionForm class."""
        self.request_user = kwargs.pop('current_user')
        # Now kwargs doesn't contain 'current_user' ==>
        # so we can safely pass it to the base class method
        super(ColectionUpdateForm, self).__init__(*args, **kwargs)

    image_manager = ImageManager()

    imageurl = forms.URLField(
        label="Colection Image URL",
        required=False,
        help_text="Formats: {}".format(image_manager.valid_extensions))

    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)

    class Meta:
        """Meta class for Colection Form."""

        # Provide an association between the ModelForm and a model
        model = Colection
        fields = ('name', 'subname', 'volume', 'editors', 'distributor',
                  'max_numbers', 'language', 'colection_type',
                  'colection_format', 'initial_number')

    def clean_imageurl(self):
        """Clean method for imageurl form field."""
        url = self.cleaned_data['imageurl']
        if url:
            if not self.image_manager.is_valid_image_extension(url):
                msg = 'The given URL does not match valid image extensions.'
                raise forms.ValidationError(msg)
        return url

    def save(self, commit=True):
        """Overrride of save method in Colection Form."""
        collection = super(ColectionUpdateForm, self).save(commit=False)

        # do custom stuff
        image_url = self.cleaned_data['imageurl']

        # download image from the given URL
        if image_url:
            response = self.image_manager.check_http_url(image_url)
            if response:
                image_type = image_url.rsplit('.', 1)[1].lower()
                image_name = slugify(collection.name) + '_' + \
                    slugify(collection.subname) + '_v' + \
                    str(collection.volume) + '_' + \
                    slugify(collection.distributor) + '.' + image_type
                # Example: daredevil_fall-from-paradise_v1_forum.jpg
                collection.image.save(image_name, ContentFile(response.read()),
                                      save=False)

        if commit:
            collection.save()
            col = Colection.objects.get(
                name=self.cleaned_data['name'],
                volume=self.cleaned_data['volume'])
            if col:
                # custom actions once the Colection is saved
                # 1.) Add all related editors
                if self.cleaned_data['editors']:
                    col.update_editors(self.cleaned_data['editors'])
                    # for editor in self.cleaned_data['editors']:
                    #     col.editors.add(editor)
                    #     col.update_editors(editors)

        return collection


class CollectionAddComicsForm(forms.ModelForm):
    """Collection Add Comics form."""

    def __init__(self, *args, **kwargs):
        """Contructor for ColectionForm class."""
        self.request_user = kwargs.pop('current_user')
        self.mycollection = kwargs.pop('current_collection')
        # Now kwargs doesn't contain current_user / current_collection ==>
        # so we can safely pass it to the base class method
        super(CollectionAddComicsForm, self).__init__(*args, **kwargs)

    full_colection = forms.BooleanField(
        label="Add comics",
        required=False,
        help_text="Fill the collection with all comics")

    input_range = forms.CharField(
        max_length=128,
        label="Range",
        required=False,
        help_text="Please enter a valid range")

    pages = forms.IntegerField(
        label="Pages",
        min_value=1,
        required=False,
        help_text='Number of pages of each comic')

    purchase_price = forms.FloatField(
        label="Purchase Price",
        required=False,
        help_text='Money paid for these comics')

    purchase_unit = forms.ChoiceField(
        label="currency",
        choices=Comic.CURRENCY_TYPES)

    retail_price = forms.FloatField(
        label="Retail Price",
        required=False,
        help_text='Real price of each comic')

    retail_unit = forms.ChoiceField(
        label="currency",
        required=True,
        choices=Comic.CURRENCY_TYPES)

    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)

    max_numbers = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False)

    class Meta:
        """Meta class for Collection Add Comics Form."""

        # Provide an association between the ModelForm and a model
        model = Colection
        fields = ('max_numbers',)

    def clean_input_range(self):
        """Clean method for input_range form field."""
        my_range = self.cleaned_data['input_range']
        max_numbers = self.cleaned_data['max_numbers']
        if my_range:
            selection, invalid = parse_int_set(inputstr=my_range,
                                               max=max_numbers)
            if invalid:
                # msg = 'Invalid input values: {}'.format(str(invalid))
                msg = 'Invalid input values: {}'.format(
                    ", ".join(str(item) for item in invalid))
                raise forms.ValidationError(msg)
        return my_range

    def save(self, commit=True):
        """Overrride of save method in Collection Add Comic Form."""
        collection = super(CollectionAddComicsForm, self).save(commit=False)

        if commit:
            col = Colection.objects.get(id=self.mycollection.id)
            if col:
                # custom actions once the Collection is saved
                # 2.) if full_colection / range  ==> Add all related comics
                if self.cleaned_data['full_colection']:
                    col.complete_colection(
                        user=self.request_user,
                        pages=self.cleaned_data['pages'],
                        retail_price=self.cleaned_data['retail_price'],
                        retail_unit=self.cleaned_data['retail_unit'],
                        purchase_price=self.cleaned_data['purchase_price'],
                        purchase_unit=self.cleaned_data['purchase_unit'])
                elif self.cleaned_data['input_range']:
                    col.complete_colection(
                        user=self.request_user,
                        rangeset=self.cleaned_data['input_range'],
                        pages=self.cleaned_data['pages'],
                        retail_price=self.cleaned_data['retail_price'],
                        retail_unit=self.cleaned_data['retail_unit'],
                        purchase_price=self.cleaned_data['purchase_price'],
                        purchase_unit=self.cleaned_data['purchase_unit'])
            # TODO: refactor previous code to make a single calling
        return collection


# ------------------------------------------------------------------ #
#
#                        Publisher Forms
#
# ------------------------------------------------------------------ #
class PublisherForm(forms.ModelForm):
    """Publisher form."""

    image_manager = ImageManager()
    name = forms.CharField(max_length=128, label="Name",
                           help_text="Please enter the Publisher name")

    history = forms.CharField(widget=forms.Textarea, max_length=3000,
                              label="History",
                              required=False, help_text="Publisher History")

    nationality = CountryField(blank_label='(select country)',
                               help_text="Nationality")

    start_date = forms.DateField(label="Beginning of Publication Date",
                                 required=False,
                                 help_text="Beginning of publications date")
    end_date = forms.DateField(label="End of publications date",
                               required=False,
                               help_text="end of publications date")
    extrainfo = forms.URLField(label="Extra Info (URL)",
                               required=False,
                               help_text="Publisher Extra Info")
    imageurl = forms.URLField(label="Publisher logo (URL)", required=False,
                              help_text="Formats: {}".format(
                                  image_manager.valid_extensions))
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        """Meta class for Publisher Form."""

        # Provide an association between the ModelForm and a model
        model = Publisher
        fields = ('name', 'history', 'nationality', 'start_date', 'end_date',
                  'extrainfo')

    def clean_imageurl(self):
        """Clean method for imageurl form field."""
        url = self.cleaned_data['imageurl']
        if url:
            if not self.image_manager.is_valid_image_extension(url):
                msg = 'The given URL does not match valid image extensions.'
                raise forms.ValidationError(msg)
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """Overrride of save method in Publisher Form."""
        publisher = super(PublisherForm, self).save(commit=False)

        image_url = self.cleaned_data['imageurl']
        # download image from the given URL
        if image_url:
            response = self.image_manager.check_http_url(image_url)
            if response:
                image_type = image_url.rsplit('.', 1)[1].lower()
                image_name = slugify(publisher.name) + '.' + image_type
                publisher.image.save(image_name, ContentFile(response.read()),
                                     save=False)
        if commit:
            publisher.save()
        return publisher


# ------------------------------------------------------------------ #
#
#                        Comic Forms
#
# ------------------------------------------------------------------ #
class ComicForm(forms.ModelForm):
    """Comic form."""

    image_manager = ImageManager()
    title = forms.CharField(max_length=128, label="Name", required=False,
                            help_text="Comic title")

    number = forms.IntegerField(label="Number", min_value=0,
                                help_text='Number')

    pages = forms.IntegerField(label="Pages", min_value=1,
                               help_text='Number of pages')

    purchase_price = forms.FloatField(label="Purchase Price",
                                      required=False,
                                      help_text='Money paid for this comic')

    purchase_unit = forms.ChoiceField(label="currency",
                                      choices=Comic.CURRENCY_TYPES)

    retail_price = forms.FloatField(label="Retail Price",
                                    required=False,
                                    help_text='Real price of comic (cover)')

    retail_unit = forms.ChoiceField(label="currency",
                                    required=True,
                                    choices=Comic.CURRENCY_TYPES)

    extrainfo = forms.URLField(label="External Info (URL)",
                               required=False,
                               help_text="Comic External Info")

    comments = forms.CharField(widget=forms.Textarea, max_length=3000,
                               label="Comments",
                               required=False,
                               help_text="Comic comments")

    pub_date = forms.DateField(label="Publication Date",
                               help_text="Colection publication date",
                               required=False)
    imageurl = forms.URLField(label="Comic Image URL", required=False,
                              help_text="Formats: {}".format(
                                  image_manager.valid_extensions))

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        """Meta class for Comic Form."""

        # Provide an association between the ModelForm and a model
        model = Comic
        fields = ('title', 'number', 'pages', 'color', 'digital', 'extrainfo',
                  'comments', 'pub_date', 'colection', 'purchase_price',
                  'purchase_unit', 'retail_price', 'retail_unit')

    def clean_imageurl(self):
        """Clean method for imageurl form field."""
        url = self.cleaned_data['imageurl']
        if url:
            if not self.image_manager.is_valid_image_extension(url):
                msg = 'The given URL does not match valid image extensions.'
                raise forms.ValidationError(msg)
        return url

    def clean_extrainfo(self):
        """Clean method for extrainfo form field."""
        url = self.cleaned_data['extrainfo']
        if url:
            response = self.image_manager.check_http_url(url)
            if not response:
                msg = 'The given URL does not match a valid link.'
                raise forms.ValidationError(msg)
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """Overrride of save method in Publisher Form."""
        comic = super(ComicForm, self).save(commit=False)

        # Image section
        image_url = self.cleaned_data['imageurl']
        # download image from the given URL
        if image_url:
            response = self.image_manager.check_http_url(image_url)
            if response:
                image_type = image_url.rsplit('.', 1)[1].lower()
                image_name = slugify(comic.colection) + \
                    '_n' + str(comic.number) + \
                    '.' + image_type

                comic.cover.save(image_name, ContentFile(response.read()),
                                 save=False)
        if commit:
            comic.save()
        return comic


class ComicUpdateForm(forms.ModelForm):
    """Comic Update form."""

    def __init__(self, *args, **kwargs):
        """Contructor for ColectionForm class."""
        self.current_user = kwargs.pop('current_user')
        self.current_comic = kwargs.pop('current_comic')
        self.purchase_price = kwargs.pop('purchase_price')
        self.purchase_unit = kwargs.pop('purchase_unit')
        # Now kwargs doesn't contain 'current_user' ==>
        # so we can safely pass it to the base class method
        super(ComicUpdateForm, self).__init__(*args, **kwargs)

    image_manager = ImageManager()
    title = forms.CharField(max_length=128, label="Name", required=False,
                            help_text="Comic title")

    pages = forms.IntegerField(label="Pages", min_value=1,
                               help_text='Number of pages')

    purchase_price = forms.FloatField(label="Purchase Price",
                                      required=False,
                                      help_text='Money paid for this comic')

    purchase_unit = forms.ChoiceField(label="currency",
                                      choices=Comic.CURRENCY_TYPES)

    retail_price = forms.FloatField(label="Retail Price",
                                    required=False,
                                    help_text='Real price of comic (cover)')

    retail_unit = forms.ChoiceField(label="currency",
                                    required=True,
                                    choices=Comic.CURRENCY_TYPES)

    extrainfo = forms.URLField(label="External Info (URL)",
                               required=False,
                               help_text="Comic External Info")

    comments = forms.CharField(widget=forms.Textarea, max_length=3000,
                               label="Comments",
                               required=False,
                               help_text="Comic comments")

    pub_date = forms.DateField(label="Publication Date",
                               help_text="Colection publication date",
                               required=False)
    imageurl = forms.URLField(label="Comic Image URL", required=False,
                              help_text="Formats: {}".format(
                                  image_manager.valid_extensions))

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        """Meta class for Comic Form."""

        # Provide an association between the ModelForm and a model
        model = Comic
        fields = ('title', 'pages', 'color', 'digital', 'extrainfo',
                  'comments', 'pub_date', 'retail_price', 'retail_unit')

    def clean_imageurl(self):
        """Clean method for imageurl form field."""
        url = self.cleaned_data['imageurl']
        if url:
            if not self.image_manager.is_valid_image_extension(url):
                msg = 'The given URL does not match valid image extensions.'
                raise forms.ValidationError(msg)
        return url

    def clean_extrainfo(self):
        """Clean method for extrainfo form field."""
        url = self.cleaned_data['extrainfo']
        if url:
            response = self.image_manager.check_http_url(url)
            if not response:
                msg = 'The given URL does not match a valid link.'
                raise forms.ValidationError(msg)
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """Overrride of save method in ComicUpdate Form."""
        comic = super(ComicUpdateForm, self).save(commit=False)

        # Image section
        image_url = self.cleaned_data['imageurl']
        cd_purchase_price = self.cleaned_data['purchase_price']
        cd_purchase_unit = self.cleaned_data['purchase_unit']
        # download image from the given URL
        if image_url:
            response = self.image_manager.check_http_url(image_url)
            if response:
                image_type = image_url.rsplit('.', 1)[1].lower()
                image_name = slugify(comic.colection) + \
                    '_n' + str(comic.number) + \
                    '.' + image_type

                comic.cover.save(image_name, ContentFile(response.read()),
                                 save=False)

        try:
            o = Ownership.objects.get(comic=self.current_comic,
                                      user=self.current_user)
            o.purchase_price = cd_purchase_price
            o.purchase_unit = cd_purchase_unit
            o.save()
        except Ownership.DoesNotExist:
            if cd_purchase_price:
                o = Ownership(comic=self.current_comic, user=self.current_user)
                o.purchase_price = cd_purchase_price
                o.purchase_unit = cd_purchase_unit
                o.save()

        if commit:
            comic.save()
        return comic


class ComicAddSagaForm(forms.ModelForm):
    """Comic Add Saga form."""

    def __init__(self, *args, **kwargs):
        """Contructor for ColectionForm class."""
        self.request_user = kwargs.pop('current_user')
        self.current_comic = kwargs.pop('current_comic')
        # Now kwargs doesn't contain 'current_user' ==>
        # so we can safely pass it to the base class method
        super(ComicAddSagaForm, self).__init__(*args, **kwargs)

    saga = forms.ModelChoiceField(
        queryset=Saga.objects.all(),
        label="Available Saga",
        help_text="Saga")

    saganumber = forms.IntegerField(
        label="Number",
        min_value=1,
        initial=1,
        help_text='Number in Saga')

    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)

    class Meta:
        """Meta class for Comic Add Saga Form."""

        # Provide an association between the ModelForm and a model
        model = Comic
        fields = ('slug',)

    def clean_saganumber(self):
        """."""
        saganame = self.cleaned_data['saga']
        number = self.cleaned_data['saganumber']

        if saganame and number:
            s = Saga.objects.get(name=saganame)
            if not s.is_available(number):
                msg = 'This number is already is use, choose a valid one.'
                raise forms.ValidationError(msg)
        return number

    def save(self, commit=True):
        """Overrride of save method in ComicAddSaga Form."""
        saga = super(ComicAddSagaForm, self).save(commit=False)

        if commit:
            saga.save()
            # Atatch the current number to the list of Saga Comics
            mysaga = Saga.objects.get(name=self.cleaned_data['saga'])
            mycomic = Comic.objects.get(slug=self.current_comic)

            comic_in_saga = ComicsInSaga()
            comic_in_saga.saga = mysaga
            comic_in_saga.comic = mycomic
            comic_in_saga.number_in_saga = self.cleaned_data['saganumber']
            comic_in_saga.save()

        return saga


# ------------------------------------------------------------------ #
#
#                        Login / Logout Forms
#
# ------------------------------------------------------------------ #
class LoginForm(forms.Form):
    """Login Form."""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# ------------------------------------------------------------------ #
#
#                        Profile Forms
#
# ------------------------------------------------------------------ #
class UserEditForm(forms.ModelForm):
    """."""

    class Meta:
        """."""

        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """."""

    class Meta:
        """."""

        model = Profile
        fields = ('date_of_birth', 'photo')


# ------------------------------------------------------------------ #
#
#                        Profile Forms
#
# ------------------------------------------------------------------ #
class SagaCreateForm(forms.ModelForm):
    """Saga Creation form."""

    def __init__(self, *args, **kwargs):
        """Contructor for SagaCreateForm class."""
        self.request_user = kwargs.pop('current_user')
        # Now kwargs doesn't contain 'current_user' ==>
        # so we can safely pass it to the base class method
        super(SagaCreateForm, self).__init__(*args, **kwargs)

    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)

    class Meta:
        """Meta class for Colection Form."""

        # Provide an association between the ModelForm and a model
        model = Saga
        fields = ('name', 'total_numbers', 'argument')


class SagaUpdateForm(forms.ModelForm):
    """Saga Update form."""

    def __init__(self, *args, **kwargs):
        """Contructor for SagaUpdateForm class."""
        self.request_user = kwargs.pop('current_user')
        # Now kwargs doesn't contain 'current_user' ==>
        # so we can safely pass it to the base class method
        super(SagaUpdateForm, self).__init__(*args, **kwargs)

    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)

    class Meta:
        """Meta class for Colection Form."""

        # Provide an association between the ModelForm and a model
        model = Saga
        fields = ('name', 'total_numbers', 'argument')
