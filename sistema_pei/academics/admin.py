from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "courses", "subject_type"]

    @admin.display(description="Cursos")
    def courses(self, obj):
        return ", ".join([course.name for course in obj.courses.all()])


class CoursesAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "course_type", "period"]


class EnrollmentAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["student", "offer"]


class OfferAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["status", "course", "subject", "year"]

    @admin.display(
        description="Professores",
    )
    def get_teachers(self, obj):
        return ", ".join([teacher.name for teacher in obj.teachers.all()])

class MatrixAdmin(admin.ModelAdmin):
    search_fields = ['name','year']
    search_help_text = _("Pesquise a matriz pelo nome ou ano")
    readonly_fields = ['updated_by','created_at']
    list_filter = ['year']
    

admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.Course, CoursesAdmin)
admin.site.register(models.Enrollment, EnrollmentAdmin)
admin.site.register(models.Offer, OfferAdmin)
admin.site.register(models.Matrix,MatrixAdmin)