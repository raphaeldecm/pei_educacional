from django.contrib import admin

from . import models


# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "subject_type", "course", "teacher"]


class CoursesAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["name", "course_type", "period"]


admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.Courses, CoursesAdmin)
