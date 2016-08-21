"""Admin models for the Comics app in the Comicteca project."""
from django.contrib import admin
from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher
from comics.models import Comic
from comics.models import Colaborator
# from comics.models import Distributor, Editor


# Register your models here.
# ------------------------------------------------------------------ #
#
#                         Inline Models
#
# ------------------------------------------------------------------ #
class ColaboratorInline(admin.TabularInline):
    """Inline for Colaborator model."""

    model = Colaborator
    extra = 1


class ComicInline(admin.TabularInline):
    """Inline for Comic model."""

    model = Comic
    exclude = ['title', 'slug', 'updated', 'inserted', 'extrainfo']
    ordering = ('number',)
    extra = 1


# ------------------------------------------------------------------ #
#
#                         Main Admin Models
#
# ------------------------------------------------------------------ #
class ArtistAdmin(admin.ModelAdmin):
    """."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'nationality', 'inserted', 'updated')


class ColectionAdmin(admin.ModelAdmin):
    """."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'subname', 'volume', 'get_colection_list',
                    'get_distributor', 'colection_type', 'inserted', 'updated')
    search_fields = ['name', 'subname']
    list_filter = ['name']
    fieldsets = [
        ('Nombre Coleccion', {'fields': ['name', 'subname', 'volume',
                                         'colection_type',
                                         'max_numbers', 'pub_date', 'slug'
                                         ]}),
        ('Editoriales', {'fields': ['distributor', 'editors']}),
    ]

    inlines = [ComicInline]

    def get_distributor(self, obj):
        """."""
        return obj.distributor.name

    def get_colection_list(self, obj):
        """."""
        return obj.colection_list()

    get_distributor.admin_order_field = 'distributor'
    get_distributor.short_description = 'Distributor Name'
    get_colection_list.short_description = 'Colection List'


class PublisherAdmin(admin.ModelAdmin):
    """."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'history', 'inserted', 'updated')
    search_fields = ['name']


class ComicAdmin(admin.ModelAdmin):
    """."""

    # prepopulated_fields = {'slug': ('name',)}
    list_display = ('get_colection_name', 'get_colection_volume',
                    'get_colection_distributor', 'number',
                    'title', 'pages', 'inserted', 'updated')
    search_fields = ['slug', 'title']
    inlines = [ColaboratorInline]

    def get_colection_name(self, obj):
        """."""
        return obj.colection.name

    def get_colection_volume(self, obj):
        """."""
        return obj.colection.volume

    def get_colection_distributor(self, obj):
        """."""
        return obj.colection.distributor

    get_colection_name.short_description = 'Colection Name'
    get_colection_volume.short_description = 'Volume'
    get_colection_distributor.short_description = 'Distributor'

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Colection, ColectionAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Comic, ComicAdmin)
admin.site.register(Colaborator)
