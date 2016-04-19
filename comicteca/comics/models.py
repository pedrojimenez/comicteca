"""Models for the comicteca project."""
from django.db import models
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify

class Artist(models.Model):
    """Artists model."""

    name = models.CharField(max_length=30)
    nationality = CountryField(blank_label='(select country)')
    birthdate = models.DateField(blank=True, null=True)
    deathdate = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    slug = models.SlugField()

    def __unicode__(self):
        """str/unicode function of Artists class."""
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Artist, self).save(*args, **kwargs)

    class Meta:
        """Meta class for Artist model."""

        db_table = 'artists'
        verbose_name_plural = "artists"
