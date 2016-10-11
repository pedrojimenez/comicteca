# duplicate the models
COPY_SUFFIX = "-copy"


def duplicate_colection(admin, request, queryset):
    for colection in queryset:
        colection.id = None
        colection.name = colection.name + COPY_SUFFIX
        colection.save()
        admin.message_user(request,
                           "Colection {} successfully duplicated.".
                           format(colection.name))

duplicate_colection.short_description = "Duplicate selected colections"
