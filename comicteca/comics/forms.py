"""Forms for Comic app."""
from django import forms
# from django.contrib.auth.models import User
# from rango.models import Page, Category, UserProfile

from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher

# from urllib3 import request
# from urllib.request import urlopen
# import urllib.request
import urllib
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django_countries.fields import CountryField


class ArtistCreateForm(forms.ModelForm):
    """Artist form."""

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
                              help_text="Formats: jpg/jpeg/png")
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
        valid_extensions = ['jpg', 'jpeg', 'png']
        if url:
            extension = url.rsplit('.', 1)[1].lower()
            if extension not in valid_extensions:
                msg = 'The given URL does not match valid image extensions.'
                raise forms.ValidationError(msg)
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """."""
        artist = super(ArtistCreateForm, self).save(commit=False)

        image_url = self.cleaned_data['imageurl']
        # download image from the given URL
        if image_url:
            # response = urllib.request.urlopen(image_url)
            # TODO try except ---> protect for a erroneous url
            response = urllib.urlopen(image_url)

            image_type = image_url.rsplit('.', 1)[1].lower()
            image_name = slugify(artist.name) + '.' + image_type

            artist.image.save(image_name, ContentFile(response.read()),
                              save=False)
        if commit:
            artist.save()
        return artist


class ColectionForm(forms.ModelForm):
    """Colection form."""

    name = forms.CharField(max_length=128, label="Name",
                           help_text="Please enter the Colection name")
    subname = forms.CharField(max_length=128, label="Name", required=False,
                              help_text="Please enter the Colection subname")
    volume = forms.IntegerField(label="Volume", min_value=1,
                                help_text='Volume')
    colection_type = forms.ChoiceField(label="Type", required="True",
                                       choices=Colection.TYPE_OF_COLECTION)

    editors = forms.ModelMultipleChoiceField(queryset=Publisher.objects.all(),
                                             help_text="Editors",
                                             label="Edition Publishers")
    distributor = forms.ModelChoiceField(queryset=Publisher.objects.all(),
                                         help_text="Distributor",
                                         label="Distribution Publishers",
                                         required=True)
    max_numbers = forms.IntegerField(label="Total numbers", min_value=0,
                                     help_text='Total numbers')
    language = CountryField(blank_label='(select country)',
                            help_text="Colection Language")
    pub_date = forms.DateField(label="Publication Date",
                               help_text="Colection publication date",
                               required=False)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        """Meta class for Colection Form."""

        # Provide an association between the ModelForm and a model
        model = Colection
        fields = ('name', 'subname', 'volume', 'editors', 'distributor',
                  'max_numbers', 'language', 'pub_date')

    def save(self, commit=True):
        """Overrride of save method in Colection Form."""
        instance = super(ColectionForm, self).save(commit=False)

        # do custom stuff
        instance.colection_type = self.cleaned_data['colection_type']

        if commit:
            instance.save()
            c = Colection.objects.get(
                name=self.cleaned_data['name'],
                volume=self.cleaned_data['volume'])
            if c:
                # custom actions once the Colection is saved
                print "Colection saved <{} v{}>".format(c.name, c.volume)

        return instance


class PublisherForm(forms.ModelForm):
    """Publisher form."""

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
                              help_text="Formats: jpg/jpeg/png")
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
        valid_extensions = ['jpg', 'jpeg', 'png']
        if url:
            extension = url.rsplit('.', 1)[1].lower()
            if extension not in valid_extensions:
                msg = 'The given URL does not match valid image extensions.'
                raise forms.ValidationError(msg)
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """."""
        publisher = super(PublisherForm, self).save(commit=False)

        image_url = self.cleaned_data['imageurl']
        # download image from the given URL
        if image_url:
            # response = urllib.request.urlopen(image_url)
            # TODO try except ---> protect for a erroneous url
            response = urllib.urlopen(image_url)

            image_type = image_url.rsplit('.', 1)[1].lower()
            image_name = slugify(publisher.name) + '.' + image_type

            publisher.image.save(image_name, ContentFile(response.read()),
                                 save=False)
        if commit:
            publisher.save()
        return publisher
