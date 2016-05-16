"""Forms for Comic app."""
from django import forms
# from django.contrib.auth.models import User
# from rango.models import Page, Category, UserProfile

from comics.models import Artist
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
