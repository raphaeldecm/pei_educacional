from django.urls import path

from sistema_pei.academics import views

app_name = "academics"
urlpatterns = [
    path("dashboard/", views.AcademicsIndexView.as_view(), name="dashboard"),
    path(
        "course/list/",
        views.CourseListView.as_view(),
        name="course_list",
    ),
    path(
        "course/create/",
        views.CourseCreateView.as_view(),
        name="course_create",
    ),
    path(
        "course/update/<int:pk>/",
        views.CourseUpdateView.as_view(),
        name="course_update",
    ),
    path(
        "course/delete/<int:pk>/",
        views.CourseDeleteView.as_view(),
        name="course_delete",
    ),
    path(
        "course/detail/<int:pk>/",
        views.CourseDetailView.as_view(),
        name="course_detail",
    ),
    path(
        "offers/list/",
        views.OffersPageView.as_view(),
        name="offer_list",
    ),
    path(
        "offers/create/",
        views.CreateOfferPageView.as_view(),
        name="offer_create",
    ),
    path(
        "offers/update/<int:pk>/",
        views.EditOfferPageView.as_view(),
        name="offer_update",
    ),
    path(
        "offers/delete/<int:pk>/",
        views.DeleteOfferView.as_view(),
        name="offer_delete",
    ),
    path(
        "offers/detail/<int:pk>/",
        views.OfferDetailsPageView.as_view(),
        name="offer_detail",
    ),
    path(
        "offers/remove_student_from_offer/<int:offer_id>/<int:student_id>/",
        views.RemoveStudentFromOfferView.as_view(),
        name="remove_student_from_offer",
    ),
    path(
        "offers/add_student_to_offer/<int:offer_id>/",
        views.AddStudentToOfferView.as_view(),
        name="add_student_to_offer",
    ),
]
