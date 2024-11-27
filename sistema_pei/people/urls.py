from django.urls import path

from sistema_pei.people import views

app_name = "people"
urlpatterns = [
    path("teacher/list/", views.TeacherListView.as_view(), name="teacher_list"),
    path("teacher/create/", views.TeacherCreateView.as_view(), name="teacher_create"),
    path("teacher/import/", views.TeacherImportView.as_view(),
    name="teacher_import",
    ),
    path(
        "teacher/update/<int:pk>/",
        views.TeacherUpdateView.as_view(),
        name="teacher_update",
    ),
    path(
        "teacher/delete/<int:pk>/",
        views.TeacherDeleteView.as_view(),
        name="teacher_delete",
    ),
    path(
        "teacher/detail/<int:pk>/",
        views.TeacherDetailView.as_view(),
        name="teacher_detail",
    ),
    path(
        "profile/<int:pk>",
        views.ProfilePageView.as_view(),
        name="profile",
    ),
    path(
        "profile/edit/<int:pk>/",
        views.EditPersonalDataView.as_view(),
        name="profile_update",
    ),
    path(
        "profile/<int:student_id>/update_student_grades/<int:enrollment_id>",
        views.UpdateStudentGradesView.as_view(),
        name="student_update_grades",
    ),
    path(
        "profile/<int:pk>/edit_historic_data/",
        views.EditHistoricPersonalDataView.as_view(),
        name="student_update_historic",
    ),
    path(
        "profile/<int:pk>/upload_files/",
        views.UploadStudentFilesView.as_view(),
        name="student_upload_files",
    ),
    path(
        "profile/<int:pk>/delete_file/",
        views.DeletePersonalFilesView.as_view(),
        name="student_delete_file",
    ),
    path(
        "student/list/",
        views.StudentListView.as_view(),
        name="student_list",
    ),
    path(
        "student/create/",
        views.StudentCreateView.as_view(),
        name="student_create",
    ),
    path(
        "student/delete/<int:pk>/",
        views.StudentDeleteView.as_view(),
        name="student_delete",
    ),
    path(
        "notification/mark_as_viewed/<int:pk>/",
        views.mark_notification_as_viewed,
        name="notification_mark_as_viewed",
    ),
    path(
        "notification/mark_all_viewed/",
        views.mark_all_notifications_as_viewed,
        name="notification_mark_all_as_viewed",
    ),
]


