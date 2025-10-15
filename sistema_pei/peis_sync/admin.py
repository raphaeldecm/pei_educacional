from django.contrib import admin

from sistema_pei.peis_sync.models import AppVersion


@admin.register(AppVersion)
class AppVersionAdmin(admin.ModelAdmin):
    list_display = ("version", "releaseDate")
    ordering = ("-releaseDate",)
    search_fields = ("version",)
    list_filter = ("releaseDate",)
