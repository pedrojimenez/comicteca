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


class Colection(models.Model):
    """Colection model."""

    name = models.CharField(max_length=50)
    subname = models.CharField(max_length=50, blank=True)
    volume = models.IntegerField(default=1)
    max_numbers = models.IntegerField(default=0)
    numbers = models.IntegerField(default=0)
    language = CountryField(blank_label='(select country)', default='ES')
    pub_date = models.DateField(blank=True, null=True)
    slug = models.SlugField()

    def __unicode__(self):
        """str/unicode function of Colection class."""
        str_temp = self.name
        if self.subname:
            str_temp = str_temp + " - " + self.subname
        str_temp = str_temp + " - Vol " + str(self.volume)
        return str_temp

    def save(self, *args, **kwargs):
        """Overwriting of save function in Colection class."""
        self.slug = slugify(self.name + ' v' + str(self.volume))
        super(Colection, self).save(*args, **kwargs)


    def colection_list(self):
        """Admin site method."""
        if (self.max_numbers != 0) and (self.max_numbers == self.numbers):
            return "Complete"
        else:
            return str(self.numbers) + "/" + str(self.max_numbers)

    class Meta:
        """Meta class for Colection model."""

        db_table = 'colections'
        verbose_name_plural = "colections"


class Publisher(models.Model):
    """Pubisher model."""

    name = models.CharField(max_length=128,primary_key=True)
    history = models.TextField(blank=True,default='')
    start_date = models.DateField('Comienzo de Editorial',blank=True,null=True)
    end_date = models.DateField('Fin de Publicaciones',blank=True,null=True)
    slug = models.SlugField()

    def __unicode__(self):
        """str/unicode function of Publisher class."""
        return self.name

    def save(self, *args, **kwargs):
        """Overwriting of save function in Publisher class."""
        self.slug = slugify(self.name)
        super(Publisher, self).save(*args, **kwargs)
