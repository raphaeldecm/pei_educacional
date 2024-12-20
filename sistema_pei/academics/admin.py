from django.contrib import admin

from . import models


# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "subject_type"]


class CoursesAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "course_type", "period"]


class EnrollmentAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["student", "grade1", "grade2", "grade3", "grade4"]


class OfferAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["status", "subject", "year"]

    @admin.display(
        description="Professores",
    )
    def get_teachers(self, obj):
        return ", ".join([teacher.name for teacher in obj.teachers.all()])


admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.Course, CoursesAdmin)
admin.site.register(models.Enrollment, EnrollmentAdmin)
admin.site.register(models.Offer, OfferAdmin)
