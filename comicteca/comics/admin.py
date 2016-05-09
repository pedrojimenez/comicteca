"""Admin models for the Comics app in the Comicteca project."""
from django.contrib import admin
from comics.models import Artist
from comics.models import Colection

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


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Colection, ColectionAdmin)

