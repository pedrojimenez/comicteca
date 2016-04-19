"""Admin models for the Comics app in the Comicteca project."""
from django.contrib import admin
from comics.models import Artist

# Register your models here.

class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Artist, ArtistAdmin)
