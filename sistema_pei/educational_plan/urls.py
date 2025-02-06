from django.urls import path

from sistema_pei.educational_plan import views

app_name = "educational_plan"
urlpatterns = [
    path(
        "peis/list/",
        views.PeiListView.as_view(),
        name="pei_list",
    ),
    path(
        "peis/update/<int:pk>/",
        views.PeiUpdateView.as_view(),
        name="pei_update",
    ),
    path(
        "peis/detail/<int:pk>/",
        views.PeiDetailView.as_view(),
        name="pei_detail",
    ),
    path(
        "peis/delete/<int:pk>/",
        views.PeiDeleteView.as_view(),
        name="pei_delete",
    ),
    path(
        "peis/markCompleted/<int:pk>/",
        views.PeiMarkCompletedView.as_view(),
        name="pei_mark_completed",
    ),
    path(
        "peis/export/<int:pk>/",
        views.PeiExportPdfView.as_view(),
        name="pei_export",
    ),
    path(
        "peis/export-preview/<int:pk>/",
        views.PeiExportPreviewView.as_view(),
        name="pei_export_preview",
    ),
    path(
        "peis/comment/create/<int:pk>/",
        views.CommentCreateView.as_view(),
        name="pei_comment_create",
    ),
    path(
        "peis/comment/delete/<int:pk>/",
        views.CommentDeleteView.as_view(),
        name="pei_comment_delete",
    ),
    path(
        "peis/answer/create/<int:parent_pk>/",
        views.AnswerCreateView.as_view(),
        name="pei_answer_create",
    ),
    path(
        "peis/answer/delete/<int:parent_pk>/",
        views.AnswerDeleteView.as_view(),
        name="pei_answer_delete",
    ),
]
