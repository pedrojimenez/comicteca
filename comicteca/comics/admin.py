"""Admin models for the Comics app in the Comicteca project."""
from django.contrib import admin
from comics.models import Artist

# Register your models here.

admin.site.register(Artist)
