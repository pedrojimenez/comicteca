"""Admin models for the Comics app in the Comicteca project."""
from django.contrib import admin
from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher

# Register your models here.

class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class ColectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name','subname','volume','colection_list')
    search_fields = ['name','subname']
    list_filter = ['name']
    fieldsets = [
            ('Nombre Coleccion', {'fields': ['name','volume','subname','max_numbers','pub_date','slug']}) ,
    ]

class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name','history','start_date','end_date')
    search_fields = ['name']

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Colection, ColectionAdmin)
admin.site.register(Publisher, PublisherAdmin)

