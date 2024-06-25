from django.contrib import admin

# Register your models here.
from . import models


class TeacherAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "email"]

class ResponsibleAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "email"]


class SpecificNecessitieAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["id", "name"]


class StudentAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "email", "responsible_person"]


class NotificationAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["title", "user", "created_at", "updated_at"]

class SectorAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Responsible, ResponsibleAdmin)
admin.site.register(models.SpecificNecessitie, SpecificNecessitieAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Notification, NotificationAdmin)
admin.site.register(models.Sector, SectorAdmin)
