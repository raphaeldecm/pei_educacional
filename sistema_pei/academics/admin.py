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

class StudentGradesAnualAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["student", "grade1", "grade2", "grade3", "grade4"]

class StudentGradesSemestralAdmin(admin.ModelAdmin):
    search_fields = ["iteraction_text"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["student", "grade1", "grade2"]


admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.StudentGradesAnual, StudentGradesAnualAdmin)
admin.site.register(models.StudentGradesSemestral, StudentGradesSemestralAdmin)
admin.site.register(models.Course, CoursesAdmin)
