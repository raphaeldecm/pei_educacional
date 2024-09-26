from django.contrib import admin

from sistema_pei.people.forms import AdminStudentForm

# Register your models here.
from . import models


class CampusAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "abbreviation"]


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "campus", "email", "user", "is_active")
    search_fields = ("name", "code", "email")
    list_filter = ("campus",)
    readonly_fields = ("user",)

    def is_active(self, obj):
        return obj.user.is_active if obj.user else False
    is_active.boolean = True
    is_active.short_description = "Usuário Ativo"

    # Sobrescreve o método save_model para garantir que o Teacher seja salvo corretamente
    def save_model(self, request, obj, form, change):
        # Chama o método save do modelo Teacher, que adiciona o grupo e sincroniza o email/nome
        super().save_model(request, obj, form, change)

    # Definir campos para exibir no formulário de edição do admin
    fieldsets = (
        (None, {
            "fields": ("name", "email", "code", "campus", "photo", "user")
        }),
    )


class CoordinatorAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "email", "campus"]


class SpecificNecessitieAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["id", "name"]


class StudentAdmin(admin.ModelAdmin):
    form = AdminStudentForm
    search_fields = ["name"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "email"]

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()


class StudentFileAdmin(admin.ModelAdmin):
    search_fields = ["student__name", "file"]
    readonly_fields = ["uploaded_at"]
    list_display = ["student", "file", "uploaded_at"]


class NotificationAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["title", "user", "created_at", "updated_at"]


admin.site.register(models.Campus, CampusAdmin)
# admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Coordinator, CoordinatorAdmin)
admin.site.register(models.SpecificNecessitie, SpecificNecessitieAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.StudentFile, StudentFileAdmin)
admin.site.register(models.Notification, NotificationAdmin)
