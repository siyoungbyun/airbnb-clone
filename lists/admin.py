from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    list_display = ("name", "user", "room_count")

    search_fields = ("name",)

    filter_horizontal = ("rooms",)
