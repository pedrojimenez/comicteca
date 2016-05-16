"""Forms for Comic app."""
from django import forms
# from django.contrib.auth.models import User
# from rango.models import Page, Category, UserProfile

from comics.models import Artist
from comics.models import Colection
from django_countries.fields import CountryField


class ArtistForm(forms.ModelForm):
    """Artist form."""

    name = forms.CharField(max_length=128, label="Name",
                           help_text="Please enter the Artist name.")
    nationality = CountryField(blank_label='(select country)',
                                help_text="Nationality")
    birthdate = forms.DateField(label="Birth Date",
                                help_text="Author birth date")
    deathdate = forms.DateField(label="Death Date",
                                help_text="Author Death date")
    biography = forms.CharField(max_length=128, label="Biography",
                                help_text="Author Biography")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        """Meta class for Artist Form."""

        # Provide an association between the ModelForm and a model
        model = Artist
        fields = ('name', 'nationality', 'birthdate', 'deathdate', 'biography')


class ColectionForm(forms.ModelForm):
    """Colection form."""

    name = forms.CharField(max_length=128, label="Name",
                           help_text="Please enter the Colection name")
    subname = forms.CharField(max_length=128, label="Name", required=False,
                           help_text="Please enter the Colection subname")
    volume = forms.IntegerField(label="Volume", min_value=1, help_text='Volume')
    max_numbers = forms.IntegerField(label="Total numbers", min_value=0,
                                     help_text='Total numbers')

    language = CountryField(blank_label='(select country)',
                                help_text="Colection Language")
    pub_date = forms.DateField(label="Publication Date",
                                help_text="Colection publication date")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        """Meta class for Colection Form."""

        # Provide an association between the ModelForm and a model
        model = Colection
        fields = ('name', 'subname', 'volume', 'max_numbers', 'language', 'pub_date')
