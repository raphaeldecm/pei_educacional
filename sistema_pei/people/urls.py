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
        "people_invite/",
        views.UsersPageView.as_view(),
        name="people_invite",
    ),
]
