# duplicate the models
COPY_SUFFIX = "-copy"


# ------------------------------------------------------------------ #
#
#                         Collection Actions
#
# ------------------------------------------------------------------ #
def duplicate_colection(admin, request, queryset):
    for colection in queryset:
        colection.id = None
        colection.name = colection.name + COPY_SUFFIX
        colection.save()
        admin.message_user(request,
                           "Colection {} successfully duplicated.".
                           format(colection.name))

duplicate_colection.short_description = "Duplicate selected colections"


# ------------------------------------------------------------------ #
#
#                         Publisher Actions
#
# ------------------------------------------------------------------ #
def duplicate_publisher(admin, request, queryset):
    for publisher in queryset:
        publisher.id = None
        publisher.name = publisher.name + COPY_SUFFIX
        publisher.save()
        admin.message_user(request,
                           "Colection {} successfully duplicated.".
                           format(publisher.name))

duplicate_publisher.short_description = "Duplicate selected publishers"


# ------------------------------------------------------------------ #
#
#                         Artist Actions
#
# ------------------------------------------------------------------ #
def duplicate_artist(admin, request, queryset):
    for artist in queryset:
        artist.id = None
        artist.name = artist.name + COPY_SUFFIX
        artist.save()
        admin.message_user(request,
                           "Colection {} successfully duplicated.".
                           format(artist.name))

duplicate_artist.short_description = "Duplicate selected artists"
