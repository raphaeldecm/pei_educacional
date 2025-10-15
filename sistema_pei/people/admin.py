from django.contrib import admin
from django.utils.html import strip_tags

from sistema_pei.people.forms import AdminStudentForm

# Register your models here.
from . import models

MAX_ITEMS = 50


class CampusAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "abbreviation"]


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "campus", "email", "user", "is_active")
    search_fields = ("name", "code", "email")
    list_filter = ("campus",)
    readonly_fields = ()

    @admin.display(
        description="Usuário Ativo",
        boolean=True,
    )
    def is_active(self, obj):
        return obj.user.is_active if obj.user else False

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "email", "code", "campus", "photo", "user"),
            },
        ),
    )


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


@admin.register(models.AlertaGlobal)
class AlertaGlobalAdmin(admin.ModelAdmin):
    list_display = (
        "mensagem_resumida",
        "data_inicio",
        "data_fim",
        "criado_em",
        "atualizado_em",
    )
    list_filter = ("data_inicio", "data_fim")
    search_fields = ("mensagem",)
    readonly_fields = ("criado_em", "atualizado_em")
    ordering = ("-data_inicio",)

    @admin.display(
        description="Mensagem",
    )
    def mensagem_resumida(self, obj):
        texto_limpo = strip_tags(obj.mensagem)
        return texto_limpo[:50] + ("..." if len(texto_limpo) > MAX_ITEMS else "")


admin.site.register(models.Campus, CampusAdmin)
admin.site.register(models.SpecificNecessitie, SpecificNecessitieAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.StudentFile, StudentFileAdmin)
admin.site.register(models.Notification, NotificationAdmin)
