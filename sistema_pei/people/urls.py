from django.urls import path

from sistema_pei.people import views

app_name = "people"
urlpatterns = [
    path("teacher/list/", views.TeacherListView.as_view(), name="teacher_list"),
    path("teacher/create/", views.TeacherCreateView.as_view(), name="teacher_create"),
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
        "profile/<int:student_id>",
        views.ProfilePageView.as_view(),
        name="profile",
    ),
    path(
        "profile/<int:student_id>/edit_personal_data/",
        views.EditPersonalDataView.as_view(),
        name="edit_personal_data",
    ),
    path(
        "profile/<int:student_id>/update_student_grades/<int:enrollment_id>",
        views.UpdateStudentGradesView.as_view(),
        name="update_student_grades",
    ),
    path(
        "profile/<int:student_id>/edit_historic_data/",
        views.EditHistoricPersonalDataView.as_view(),
        name="edit_personal_historic_data",
    ),
    path(
        "profile/<int:student_id>/upload_files/",
        views.UploadStudentFilesView.as_view(),
        name="upload_files",
    ),
    path(
        "profile/<int:student_id>/delete_file/",
        views.DeletePersonalFilesView.as_view(),
        name="delete_personal_file",
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
]
