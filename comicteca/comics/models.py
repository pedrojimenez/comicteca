"""Models for the comicteca project."""
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify


# ------------------------------------------------------------------ #
#
#                         Artist Model
#
# ------------------------------------------------------------------ #
class Artist(models.Model):
    """Artists model."""

    name = models.CharField(max_length=30)
    nationality = CountryField(blank_label='(select country)')
    birthdate = models.DateField(blank=True, null=True)
    deathdate = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    slug = models.SlugField()

    def get_absolute_url(self):
        """."""
        # return reverse('artist-detail', kwargs={'pk': self.pk})
        return reverse('artist_detail', kwargs={'artist_name_slug': self.slug})

    def __unicode__(self):
        """str/unicode function of Artists class."""
        return self.name

    def save(self, *args, **kwargs):
        """Overriding of save method for Artist model."""
        self.slug = slugify(self.name)
        self.updated = timezone.now()
        super(Artist, self).save(*args, **kwargs)

    class Meta:
        """Meta class for Artist model."""

        # db_table = 'artists'
        ordering = ('-inserted',)
        verbose_name_plural = "artists"
        unique_together = ("name", "nationality", "birthdate")


# ------------------------------------------------------------------ #
#
#                         Publisher Model
#
# ------------------------------------------------------------------ #
class Publisher(models.Model):
    """Pubisher model."""

    name = models.CharField(max_length=128)
    history = models.TextField(blank=True, default='')
    start_date = models.DateField('Comienzo de Editorial', blank=True,
                                  null=True)
    end_date = models.DateField('Fin de Publicaciones', blank=True,
                                null=True)
    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    slug = models.SlugField()

    def get_absolute_url(self):
        """."""
        # return reverse('artist-detail', kwargs={'pk': self.pk})
        return reverse('publisher_detail',
                       kwargs={'publisher_name_slug': self.slug})

    def __unicode__(self):
        """str/unicode function of Publisher class."""
        return self.name

    def save(self, *args, **kwargs):
        """Overriding of save function in Publisher class."""
        self.slug = slugify(self.name)
        self.updated = timezone.now()
        super(Publisher, self).save(*args, **kwargs)


# ------------------------------------------------------------------ #
#
#                         Colection Model
#
# ------------------------------------------------------------------ #
class Colection(models.Model):
    """Colection model."""

    TYPE_OF_COLECTION = (
        ('Regular', 'Regular Serie'),
        ('Limited', 'Limited Serie'),
        ('Special', 'Special Number'),
    )
    name = models.CharField(max_length=50)
    subname = models.CharField(max_length=50, blank=True)
    volume = models.IntegerField(default=1)
    max_numbers = models.IntegerField(default=0)
    colection_type = models.CharField('Type', max_length=15,
                                      choices=TYPE_OF_COLECTION,
                                      default='Regular')
    numbers = models.IntegerField(default=0)
    language = CountryField(blank_label='(select country)', default='ES')
    pub_date = models.DateField(blank=True, null=True)
    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    slug = models.SlugField()

    # Relations
    distributor = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                    default='Marvel')
    # distributors = models.ManyToManyField('Publisher',
    #                                       related_name='Distributors',
    #                                       through='Distributor')
    editors = models.ManyToManyField(Publisher,
                                     related_name='Publishers')
    #                                through='Editor')

    def __unicode__(self):
        """str/unicode function of Colection class."""
        str_temp = self.name
        if self.subname:
            str_temp = str_temp + " - " + self.subname
        str_temp = str_temp + " - Vol " + str(self.volume)
        return str_temp

    def save(self, *args, **kwargs):
        """Overriding of save function in Colection class."""
        self.slug = slugify(self.name + ' v' + str(self.volume))
        self.updated = timezone.now()

        self.numbers = len(Comic.objects.filter(
            colection__name=self.name,
            colection__volume=self.volume))
        super(Colection, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """."""
        # return reverse('artist-detail', kwargs={'pk': self.pk})
        return reverse('colection_detail',
                       kwargs={'colection_name_slug': self.slug})

    def update_comics_number(self):
        """Count number of colection comics and return it."""
        self.numbers = len(Comic.objects.filter(colection__name=self.name,
                                                colection__volume=self.volume))

    def colection_list(self):
        """Count number of colection comics and return string."""
        if (self.max_numbers != 0) and (self.max_numbers == self.numbers):
            return "Complete"
        else:
            return str(self.numbers) + "/" + str(self.max_numbers)

    def editor_list(self):
        """Return the list of Editors as a string."""
        editor_list_output = []
        for editor in self.editors.all():
            editor_list_output.append(editor.name)

        return ', '.join(editor_list_output)

    class Meta:
        """Meta class for Colection model."""

        # db_table = 'colections'
        verbose_name_plural = "colections"
        unique_together = ("name", "volume")


# ------------------------------------------------------------------ #
#
#                         Comic Model
#
# ------------------------------------------------------------------ #
class Comic(models.Model):
    """Comic model."""

    title = models.CharField(max_length=128, blank=True, null=True)
    number = models.IntegerField(default=1)
    pages = models.IntegerField(default=24)
    slug = models.SlugField()
    colection = models.ForeignKey(Colection, on_delete=models.CASCADE)
    extrainfo = models.CharField(max_length=128, blank=True, null=True)
    pub_date = models.DateField(blank=True, null=True)
    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)

    # Relations
    colaborators = models.ManyToManyField(Artist, through='Colaborator')

    class Meta:
        """Meta class for Comic model."""

        # db_table = 'comics'
        verbose_name_plural = "comics"
        unique_together = ("colection", "number")

    def __unicode__(self):
        """str/unicode function of Comic class."""
        return self.slug

    def save(self, *args, **kwargs):
        """Overriding of save function in Comics class."""
        slugify(self.colection.slug) + '_n' + str(self.number)
        self.slug = slugify(self.colection.slug) + '_n' + str(self.number)
        self.updated = timezone.now()
        super(Comic, self).save(*args, **kwargs)
        # Update Colection "number of comics"
        self.colection.update_comics_number()


# ------------------------------------------------------------------ #
#
#                        Colaborator Model
#
# ------------------------------------------------------------------ #
class Colaborator(models.Model):
    """Colaborator model."""

    ROLE_IN_COMIC = (
        ('Guion', 'Guion'),
        ('Dibujo', 'Dibujo'),
        ('Tinta', 'Tinta'),
        ('Color', 'Color'),
        ('Color Ordenador', 'Color Ordenador'),
        ('Dialogos', 'Dialogos'),
        ('Portada', 'Portada'),
        ('Argumento', 'Argumento'),
        ('Adaptacion', 'Adaptacion'),
    )
    comic = models.ForeignKey(Comic)
    artist = models.ForeignKey(Artist)
    extrainfo = models.CharField(max_length=128, blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLE_IN_COMIC,
                            default='Guion')

    class Meta:
        """Meta class for Colaborator model."""

        unique_together = ('comic', 'artist', 'role')

    def __unicode__(self):
        """str/unicode function of Comic class."""
        return str(self.artist) + " - "\
            + str(self.comic) + " - "\
            + str(self.role)

# class Distributor(models.Model):
#     """Distributor intermediate model."""
#
#     colection = models.ForeignKey(Colection, default=4)
#     editorial = models.ForeignKey(Publisher)
#     extrainfo = models.CharField(max_length=128, blank=True, null=True)
#     principal = models.BooleanField('Principal', default=True)
#
#     class Meta:
#         """Meta class for intermediate Distributor model."""
#
#         auto_created = True
#
#
# class Editor(models.Model):
#     """Editor intermediate model."""
#
#     colection = models.ForeignKey(Colection, default=4)
#     editorial = models.ForeignKey(Publisher)
#     extrainfo = models.CharField(max_length=128, blank=True, null=True)
#     principal = models.BooleanField('Principal', default=True)
#
#     class Meta:
#         """Meta class for intermediate Editor model."""
#
#         auto_created = True
#         #db_table = 'colections_editors'
