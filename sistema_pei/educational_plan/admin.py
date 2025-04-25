from django.contrib import admin

# Register your models here.
from . import models


class PeiAdmin(admin.ModelAdmin):
    search_fields = ["enrollment"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["enrollment", "status"]
    list_filter = ["status", "enrollment"]


class FeedbackAdmin(admin.ModelAdmin):
    search_fields = ["pei"]
    readonly_fields = ["updated_by", "created_at"]


class CommentAdmin(admin.ModelAdmin):
    search_fields = ["pei"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["pei", "date"]


class AnswerAdmin(admin.ModelAdmin):
    search_fields = ["comment"]
    readonly_fields = ["updated_by", "created_at"]
    list_display = ["comment", "date"]


admin.site.register(models.Pei, PeiAdmin)
admin.site.register(models.FeedbackPei, FeedbackAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Answer, AnswerAdmin)
