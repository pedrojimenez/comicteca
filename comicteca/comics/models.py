"""Models for the comicteca project."""
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.encoding import force_text

from django_countries.fields import CountryField

from comics.storage import OverwriteStorage
from comics.utils import parse_int_set


# ------------------------------------------------------------------ #
#
#                        Saga Model
#
# ------------------------------------------------------------------ #
class Saga(models.Model):
    """Colaborator model."""

    name = models.CharField(max_length=50)
    total_numbers = models.IntegerField(default=1)
    argument = models.TextField(blank=True, null=True, max_length=3000)
    slug = models.SlugField()

    def __unicode__(self):
        """str/unicode function of Profile class."""
        return force_text(self.name)

    def save(self, *args, **kwargs):
        """Overriding of save function in Saga class."""
        self.slug = slugify(self.name)
        super(Saga, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the absolute url of Saga model."""
        # return reverse('artist-detail', kwargs={'pk': self.pk})
        return reverse('saga_detail',
                       kwargs={'saga_slug': self.slug})

    @property
    def my_image(self):
        """Return the absolute url of colection image as property.

        If the colection has no image it will search in all the comics
        but if no image is found, it will return the empty image url
        """
        # comics_set = Comic.objects.filter(colection__id=self.id)
        comics_set = Comic.objects.filter(my_sagas__id=self.id)
        for comic in comics_set:
            if comic.cover:
                return comic.cover
        return "images/noimage.png"

    def get_saga_status(self):
        """."""
        # current_numbers = ComicsInSaga.objects(saga=self.id)
        current_numbers = Comic.objects.filter(my_sagas__id=self.id).count()
        if current_numbers == self.total_numbers:
            return "Complete (" + str(current_numbers) + ")"
        else:
            return str(current_numbers) + " / " + str(self.total_numbers)

    def get_saga_pubdate(self):
        """."""
        comics_set = Comic.objects.filter(my_sagas__id=self.id)
        for comic in comics_set:
            if comic.pub_date:
                return comic.pub_date
        return "N/A"

    def get_saga_totalpages(self):
        """."""
        comics_set = Comic.objects.filter(my_sagas__id=self.id)
        totalpages = 0
        for comic in comics_set:
            totalpages += comic.pages
        return totalpages

    def get_saga_comics(self):
        """Return the comics and saga_number of each one of the Saga."""
        saga_comics = ComicsInSaga.objects.filter(saga=self.id).order_by(
            'number_in_saga')

        comic_tuple_list = []
        for saga in saga_comics:
            c = Comic.objects.get(id=saga.comic.id)
            tup = (c, saga.number_in_saga)
            comic_tuple_list.append(tup)

        return comic_tuple_list

    def get_saga_currency(self, unit='euros', output_format='string',
                          currency_type='retail'):
        """Return the total price of Colection (retail or paid)."""
        col_comics = Comic.objects.filter(my_sagas__id=self.id)
        total_currency = 0
        for comic in col_comics:
            total_currency += comic.get_price(unit, currency_type)
        if output_format == 'string':
            return str(total_currency) + ' ' + str(unit)
        return total_currency

    def is_available(self, number):
        """Check if comic number is already is use."""
        saga_comics = ComicsInSaga.objects.filter(saga=self.id).order_by(
            'number_in_saga')

        print ""
        print "SagaComics: ", saga_comics

        for comic in saga_comics:
            if number == comic.number_in_saga:
                return False
        return True


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
                              storage=OverwriteStorage(),
                              blank=True, null=True)
    slug = models.SlugField()

    def get_absolute_url(self):
        """."""
        # return reverse('artist-detail', kwargs={'pk': self.pk})
        return reverse('artist_detail', kwargs={'artist_name_slug': self.slug})

    def __unicode__(self):
        """str/unicode function of Artists class."""
        return force_text(self.name)

    def save(self, *args, **kwargs):
        """Overriding of save method for Artist model."""
        self.name = force_text(self.name).title()
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
                              storage=OverwriteStorage(),
                              blank=True, null=True)
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

        output: list[tuples(ColectionObject, "Publisher.Roles")]
        output: [(<Colection: Vengadores - Vol 1>, "editor")]
        output: [(<Colection: Naruto - Vol 3>, "editor,distributor")]
        """
        # print "xxxxxx get colaborations of Publisher: {}".format(self.name)
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
        return force_text(self.name)

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

    FORMAT_OF_COLLECTION = (
        ('Grapa', 'Grapa'),
        ('Retapado', 'Retapado'),
        ('Rustica', 'Rustica'),
        ('Cartone', 'Cartone'),
        ('Oversize', 'Oversize'),
    )

    name = models.CharField(max_length=100)
    subname = models.CharField(max_length=100, blank=True)
    volume = models.IntegerField(default=1)
    language = CountryField(blank_label='(select country)', default='ES')
    initial_number = models.IntegerField(default=1)
    max_numbers = models.IntegerField(default=0)
    colection_type = models.CharField('Type', max_length=15,
                                      choices=TYPE_OF_COLECTION,
                                      default='Regular')
    colection_format = models.CharField('Format', max_length=15,
                                        choices=FORMAT_OF_COLLECTION,
                                        default='Grapa')
    numbers = models.IntegerField(default=0)

    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='', upload_to='images/colections/',
                              storage=OverwriteStorage(),
                              blank=True, null=True)
    slug = models.SlugField()

    # Relations
    distributor = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                    default=1)
    editors = models.ManyToManyField(Publisher,
                                     related_name='Publishers')

    @property
    def my_url(self):
        """Return the absolute url as model property."""
        return self.get_absolute_url()

    @property
    def my_pub_date(self):
        """Return the Pub Date of the first comic of the Collection."""
        comics_set = Comic.objects.filter(colection__id=self.id)
        for comic in comics_set:
            if comic.pub_date:
                return comic.pub_date
        return "N/A"

    @property
    def my_image(self):
        """Return the absolute url of colection image as property.

        If the colection has no image it will search in all the comics
        but if no image is found, it will return the empty image url
        """
        if self.image:
            return self.image
        comics_set = Comic.objects.filter(colection__id=self.id)
        for comic in comics_set:
            if comic.cover:
                return comic.cover
        return "images/noimage.png"

    def __unicode__(self):
        """str/unicode function of Colection class."""
        str_temp = self.name
        if self.subname:
            str_temp += " - " + self.subname
        str_temp += " - Vol " + str(self.volume)
        str_temp += " - " + str(self.distributor)
        #return str_temp.decode('utf-8', 'ignore')
        return force_text(str_temp)

    def save(self, *args, **kwargs):
        """Overriding of save function in Colection class."""
        tmp_slug = slugify(self.name)
        if self.subname:
            tmp_slug += '-' + slugify(self.subname)
        tmp_slug += '-' + slugify(self.distributor)
        tmp_slug += '-v' + slugify(self.volume)
        self.slug = tmp_slug
        self.updated = timezone.now()

        self.numbers = len(Comic.objects.filter(
            colection__name=self.name,
            colection__volume=self.volume,
            colection__distributor=self.distributor))
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
            return "Complete ({})".format(self.max_numbers)
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

    def get_currency(self, unit='euros', output_format='string',
                     currency_type='retail'):
        """Return the total price of Colection (retail or paid)."""
        col_comics = Comic.objects.filter(colection__id=self.id)
        total_currency = 0
        for comic in col_comics:
            total_currency += comic.get_price(unit, currency_type)
        if output_format == 'string':
            return str(total_currency) + ' ' + str(unit)
        return total_currency

    def get_paid(self):
        """Return the total amount of money paid for all collection comics."""
        return self.get_currency(unit='euros', currency_type='purchase')

    def get_comics(self):
        """Return the comics of the Colection."""
        return Comic.objects.filter(colection__id=self.id)

    def get_pages(self, unit='euros'):
        """Return the total of associated comics pages."""
        col_comics = Comic.objects.filter(colection__id=self.id)
        total_pages = 0
        for comic in col_comics:
            total_pages += comic.pages
        return total_pages

    def get_missing_comics(self):
        """Return the list of missing comics."""
        missing_list = []
        for i in range(self.initial_number,
                       self.initial_number + self.max_numbers):
            try:
                Comic.objects.get(colection=self, number=i)
            except Comic.DoesNotExist:
                missing_list.append(i)
        return missing_list

    def update_editors(self, editor_list=[]):
        """Return the total of associated comics prices."""
        if self.editors == editor_list:
            return

        for editor in self.editors.all():
            if editor not in editor_list:
                self.editors.remove(editor)

        for editor in editor_list:
            if editor not in self.editors.all():
                self.editors.add(editor)

    def complete_colection(self, pages=24, rangeset=None, user=None,
                           retail_price=0, retail_unit='euros',
                           purchase_price='0', purchase_unit='euros'):
        """Complete all missing comics for the colection."""
        current_user = User.objects.get(username=user)
        localrange = set()
        invalidrange = set()
        if not rangeset:
            for i in range(self.initial_number,
                           self.initial_number + self.max_numbers):
                localrange.add(int(i))
        else:
            localrange, invalidrange = parse_int_set(rangeset,
                                                     self.max_numbers)

        # for n in range(1, self.max_numbers + 1):
        for n in range(0, len(localrange)):
            number = localrange.pop()
            print "[{}] - Adding comic #{} to collection {}".format(
                user, number, self)
                #.name.decode('utf-8', 'ignore'))

            try:
                current_comic = Comic.objects.get(
                    colection=self, number=number)
            except Comic.DoesNotExist:
                current_comic = None

            if not current_comic:
                comic = Comic()
                comic.number = number
                comic.pages = pages
                comic.colection = self
                comic.retail_price = retail_price
                comic.retail_unit = retail_unit
                comic.purchase_price = purchase_price
                comic.purchase_unit = purchase_unit
                comic.save()
                # o = Ownership(comic=current_comic, user=current_user)
                # o.purchase_price = purchase_price
                # o.purchase_unit = purchase_unit
                # o.save()
                current_comic = comic
            else:
                # TODO: Use logger instead of prints
                print "   --> Comic already exists, omitting ..."

            # Update the ownership (if not exist)
            try:
                o = Ownership.objects.get(comic=current_comic,
                                          user=current_user)
                print "   --> Comic {} already owned by <{}>".format(
                    current_comic, current_user)

            except Ownership.DoesNotExist:
                o = Ownership(comic=current_comic, user=current_user)
                print "   --> Dup. Comic <{}> now also owned by <{}>".\
                    format(current_comic, current_user)

            o.purchase_price = purchase_price
            o.purchase_unit = purchase_unit
            o.save()

        self.update_comics_number()

    class Meta:
        """Meta class for Colection model."""

        # db_table = 'colections'
        verbose_name_plural = "colections"
        unique_together = ("name", "volume", "distributor")


# ------------------------------------------------------------------ #
#
#                         Comic Model
#
# ------------------------------------------------------------------ #
class Comic(models.Model):
    """Comic model."""

    # TODO: extract it to settings
    CURRENCY_TYPES = (
        ('euros', 'euros'),
        ('pesetas', 'pesetas'),
        ('dollars', 'dollars'),
        ('pounds', 'pounds'),
    )
    # TODO: extract it to settings
    EURO_PTAS_EXCHANGE_RATE = 166.386
    EURO_DOLLARS_EXCHANGE_RATE = 1
    EURO_POUNDS_EXCHANGE_RATE = 1

    title = models.CharField(max_length=128, blank=True, null=True)
    number = models.IntegerField(default=1)
    pages = models.IntegerField(default=24)
    digital = models.BooleanField(default=False)
    color = models.BooleanField(default=True)
    slug = models.SlugField()

    # texts
    comments = models.TextField(blank=True, null=True, default='')
    extrainfo = models.URLField(blank=True, null=True)

    # dates
    pub_date = models.DateField(blank=True, null=True)
    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)

    # prices
    purchase_price = models.FloatField(default=0)
    purchase_unit = models.CharField('Type', max_length=15,
                                     choices=CURRENCY_TYPES,
                                     default='euros')
    retail_price = models.FloatField(default=0)
    retail_unit = models.CharField('Type', max_length=15,
                                   choices=CURRENCY_TYPES,
                                   default='euros')

    # cover (image)
    cover = models.ImageField(default='', upload_to='images/comics/',
                              storage=OverwriteStorage(),
                              blank=True, null=True)
    # Relations
    colection = models.ForeignKey(Colection, on_delete=models.CASCADE)
    colaborators = models.ManyToManyField(Artist, through='Colaborator')

    my_users = models.ManyToManyField(User, through='Ownership')

    my_sagas = models.ManyToManyField(Saga, through='ComicsInSaga')

    class Meta:
        """Meta class for Comic model."""

        # db_table = 'comics'
        verbose_name_plural = "comics"
        unique_together = ("colection", "number")

    @property
    def my_url(self):
        """Return the absolute url as model property."""
        return self.get_absolute_url()

    def my_cover(self):
        """Return the absolute url of comic cover as property.

        If the comic has no cover  it will return the empty image url
        """
        if self.cover:
            return self.cover
        # TODO: create an empty image with font-awesome icons
        return "images/noimage.png"

    def __unicode__(self):
        """str/unicode function of Comic class."""
        return self.slug

    def save(self, *args, **kwargs):
        """Overriding of save function in Comics class."""
        self.slug = slugify(self.colection.slug) + '-n' + str(self.number)
        self.updated = timezone.now()

        # Update prices (check if comic has purchase price but not retail)
        #               ( ==> force retail = purchase )
        if self.retail_price == 0.0 and self.purchase_price > 0:
            self.retail_price = self.purchase_price
            self.retail_unit = self.purchase_unit

        super(Comic, self).save(*args, **kwargs)

        # Update Colection "number of comics"
        self.colection.update_comics_number()

    def get_absolute_url(self):
        """Get the absolute url a comic model."""
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

    def get_sagas(self):
        """Return the list of users owning the comic."""
        return self.my_sagas.all().distinct()

    def get_users(self):
        """Return the list of users owning the comic."""
        return User.objects.filter(ownership__comic=self.id)

    def get_color(self):
        """Return if comic is printed in color or black/white."""
        if not self.color:
            return "B/W"
        return "Color"

    def get_pub_date(self):
        """Return the comic pub_date formatted."""
        # TODO: format the output of PubDate
        return self.pub_date

    def check_user(self, user):
        """Return if current comic is owned by user."""
        if user in self.my_users.all():
            return True
        return False

    def get_price(self, unit='euros', currency_type='retail'):
        """Return the selected Comic price (retail or paid)."""
        if currency_type == 'retail':
            return self.price_retail(unit=unit)
        return self.price_purchase(unit=unit)

    # Next 2 functions are used in templates and "get_price" method
    def price_retail(self, unit='euros'):
        """Return the comic real price in the desired unit."""
        if self.retail_price == 0.0:
            return 0.0

        if unit == self.retail_unit:
            return self.retail_price

        return self.__convert_to(unit=unit, price='retail')
        # return self.__convert_to(unit=unit, price=self.retail_price)

    def price_purchase(self, unit='euros'):
        """Return the comic purchase price in the desired unit."""
        # TODO: REFAACTOR with Ownership class
        if self.purchase_price == 0.0:
                return 0.0

        if unit == self.purchase_unit:
            return self.purchase_price

        return self.__convert_to(unit=unit, price='purchase')

    def __convert_to(self, price='retail', unit='euros'):
        """Convert the amount(self) into selected unit."""
        # TODO: convert to all possible units by downloading the EX_rates
        if price == 'retail':
            my_price = self.retail_price
            my_unit = self.retail_unit
        else:
            my_price = self.purchase_price
            my_unit = self.purchase_unit

        print "Converting <{} {}> to {}".format(my_price, my_unit, unit)
        if unit == 'euros':
            if my_unit == 'pesetas':
                return round(my_price / self.EURO_PTAS_EXCHANGE_RATE, 2)

            elif my_unit == 'dollars':
                return round(my_price / self.EURO_DOLLARS_EXCHANGE_RATE, 2)

            elif my_unit == 'pounds':
                return round(my_price / self.EURO_POUNDS_EXCHANGE_RATE, 2)

        elif unit == 'pesetas':
            if my_unit == 'euros':
                return round(my_price * self.EURO_PTAS_EXCHANGE_RATE, 2)

        else:
            return round(float(my_price), 2)


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
        tmp_string = str(self.artist) + " - "\
            + str(self.comic) + " - "\
            + str(self.role)
        return force_text(tmp_string)


# ------------------------------------------------------------------ #
#
#                        Profile Model
#
# ------------------------------------------------------------------ #
class Profile(models.Model):
    """Colaborator model."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(default='', upload_to='images/users/',
                              storage=OverwriteStorage(),
                              blank=True, null=True)

    def __unicode__(self):
        """str/unicode function of Profile class."""
        return 'Profile for user {}'.format(self.user.username)


# ------------------------------------------------------------------ #
#
#                    ComicsSaga intermediate Class
#
# ------------------------------------------------------------------ #
class ComicsInSaga(models.Model):
    """ComicsInSaga model."""

    comic = models.ForeignKey(Comic)
    saga = models.ForeignKey(Saga)
    number_in_saga = models.IntegerField(default=1)

    class Meta:
        """Meta class for Colaborator model."""

        unique_together = ('saga', 'number_in_saga')

    def __unicode__(self):
        """str/unicode function of Comic class."""
        tmp_string = str(self.saga) + " - "\
            + str(self.number_in_saga) + " - "\
            + str(self.comic)
        return force_text(tmp_string)


# ------------------------------------------------------------------ #
#
#                    Ownership intermediate Class
#
# ------------------------------------------------------------------ #
class Ownership(models.Model):
    """Ownership model."""

    comic = models.ForeignKey(Comic)
    user = models.ForeignKey(User)
    purchase_price = models.FloatField(default=0)
    purchase_unit = models.CharField(
        'Unit',
        max_length=15,
        choices=Comic.CURRENCY_TYPES,
        default='euros')

    class Meta:
        """Meta class for Ownership model."""

        unique_together = ('comic', 'user')

    def __unicode__(self):
        """str/unicode function of Comic class."""
        tmp_string = str(self.comic) + " - "\
            + str(self.user) + " - "\
            + str(self.purchase_price)
        return force_text(tmp_string)


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
