"""Models for the comicteca project."""
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify
from comics.storage import OverwriteStorage


# ------------------------------------------------------------------ #
#
#                         Artist Model
#
# ------------------------------------------------------------------ #
class Artist(models.Model):
    """Artists model."""

    name = models.CharField(max_length=30)
    nationality = CountryField(blank_label='(select country)', default='ES')
    birthdate = models.DateField(blank=True, null=True)
    deathdate = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True, max_length=3000)
    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    extrainfo = models.URLField(blank=True, null=True)
    image = models.ImageField(default='', upload_to='images/artists/',
                              storage=OverwriteStorage())
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
        self.name = str(self.name).title()
        self.slug = slugify(self.name)
        self.updated = timezone.now()
        super(Artist, self).save(*args, **kwargs)

    def get_colaborations_count(self):
        """Get the count of colaborations in comics of the Author."""
        comic_count = Comic.objects.filter(
            colaborators__id=self.id).distinct().count()
        return comic_count

    def get_colaborations(self):
        """Get a list of tuples with comics/role of the Author.

        ouput:  list[tuples(ComicObject, "Artist.Roles")]
        output: [(<Comic: juez-dredd-v1_n1>, "Dibujo,Guion")]
        """
        comic_list_partial = Comic.objects.filter(
            colaborators__id=self.id).distinct()
        comic_tuple = ()
        comic_list = []
        for comic in comic_list_partial:
            role_list = comic.get_artist_roles(self.id)
            comic_tuple = (comic, role_list)
            comic_list.append(comic_tuple)
        return comic_list

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
    nationality = CountryField(blank_label='(select country)', default='ES')
    history = models.TextField(blank=True, default='')
    start_date = models.DateField('Comienzo de Editorial', blank=True,
                                  null=True)
    end_date = models.DateField('Fin de Publicaciones', blank=True,
                                null=True)
    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    extrainfo = models.URLField(blank=True, null=True)
    image = models.ImageField(default='', upload_to='images/publishers/',
                              storage=OverwriteStorage())
    slug = models.SlugField()

    def get_absolute_url(self):
        """."""
        # return reverse('artist-detail', kwargs={'pk': self.pk})
        return reverse('publisher_detail',
                       kwargs={'publisher_name_slug': self.slug})

    def get_colections_distributions_count(self):
        """Get the count of colaborations in colections of the Publisher."""
        colection_count = Colection.objects.filter(
            distributor__id=self.id).distinct().count()
        return colection_count

    def get_colections_editions_count(self):
        """Get the count of colaborations in colections of the Publisher."""
        colection_count = Colection.objects.filter(
            editors__id=self.id).distinct().count()
        return colection_count

    def get_colaborations(self):
        """Get a list of tuples with colections/relation of the Publisher.

        ouput:  list[tuples(ColectionObject, "Publisher.Roles")]
        output: [(<Colection: Vengadores - Vol 1>, "editor")]
        output: [(<Colection: Naruto - Vol 3>, "editor,distributor")]
        """
        print "xxxxxx get colaborations of Publisher: {}".format(self.name)
        distributor_list_partial = Colection.objects.filter(
            distributor__id=self.id).distinct()

        editor_list_partial = Colection.objects.filter(
            editors__id=self.id).distinct()

        # Join both querysets and get a single copy of each
        colection_list_partial = distributor_list_partial | editor_list_partial
        colection_list_partial = colection_list_partial.distinct()

        colection_tuple = ()
        colection_list = []
        for colection in colection_list_partial:
            role_list = colection.get_publisher_roles(self.id)
            colection_tuple = (colection, role_list)
            colection_list.append(colection_tuple)

        return colection_list

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
    language = CountryField(blank_label='(select country)', default='ES')
    max_numbers = models.IntegerField(default=0)
    colection_type = models.CharField('Type', max_length=15,
                                      choices=TYPE_OF_COLECTION,
                                      default='Regular')
    numbers = models.IntegerField(default=0)

    pub_date = models.DateField(blank=True, null=True)
    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='', upload_to='images/artists/',
                              storage=OverwriteStorage())
    slug = models.SlugField()

    # Relations
    distributor = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                    default='Marvel')
    editors = models.ManyToManyField(Publisher,
                                     related_name='Publishers')

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
        self.save()

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

    def get_publisher_roles(self, publisher_id):
        """Return the list of roles/relation of a given Publisher."""
        role_list = []
        if self.distributor.id == publisher_id:
            role_list.append('distributor')

        for editor in self.editors.all():
            if publisher_id == editor.id:
                role_list.append('editor')
        return ','.join(role_list)

    def complete_colection(self, pages=24):
        """Complete all missing comics for the colection."""
        for n in range(1, self.max_numbers + 1):
            print "Filling comic n{} in colection {}".format(n, self.name)

            try:
                checkcomic = Comic.objects.get(colection=self, number=n)
            except Comic.DoesNotExist:
                checkcomic = None

            if not checkcomic:
                comic = Comic()
                comic.number = n
                comic.pages = pages
                comic.colection = self
                comic.save()
            else:
                print "Comic already exists, omitting . . ."
        self.update_comics_number()

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

    def get_absolute_url(self):
        """."""
        return reverse('comic_detail',
                       kwargs={'comic_name_slug': self.slug})

    def get_all_artists_roles(self):
        """Get the full list of Artists and Roles for this comic."""
        all_colaborators_list = Colaborator.objects.filter(
            comic=self.id)
        colaborator_list_partial = all_colaborators_list.values_list(
            'artist', flat=True).distinct()
        # Input: [<Colaborator: Jim Lee - juez-dredd-v1_n1 - Guion>,
        #         <Colaborator: Jim Lee - juez-dredd-v1_n1 - Dibujo>,
        #         <Colaborator: John Byrne - juez-dredd-v1_n1 - Tinta>]
        # Output: [(6,), (7,)] (ids of Artists Jim Lee and John Byrne)
        # Output: [6, 7] (with flat=true)
        #
        colaborator_tuple = ()
        colaborator_list = []
        for colaborator in colaborator_list_partial:
            artist = Artist.objects.get(id=colaborator)
            role_list = self.get_artist_roles(artist.id)
            # role_list = self.get_artist_roles(colaborator.1)
            colaborator_tuple = (artist, role_list)
            colaborator_list.append(colaborator_tuple)
        return colaborator_list

    def get_artist_roles(self, author_id):
        """Return the list of roles of a given Author."""
        colaborations = Colaborator.objects.filter(
            artist=author_id,
            comic=self.id)
        role_list = []
        for role in colaborations.values('role'):
            role_list.append(role['role'])
        return ','.join(role_list)


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
