from django.contrib.auth.decorators import login_required
from django.urls import path

from sistema_pei.academics import views

app_name = "academics"
urlpatterns = [
    path("dashboard/", views.AcademicsIndexView.as_view(), name="dashboard"),
    path(
        "courses/",
        views.CoursesPageView.as_view(),
        name="courses",
    ),
    path(
        "courses/create",
        login_required(views.CreateCoursesPageView.as_view()),
        name="create_course",
    ),
    path(
        "courses/edit/<int:course_id>",
        login_required(views.EditCoursePageView.as_view()),
        name="edit_course",
    ),
    path(
        "courses/delete/<int:course_id>",
        login_required(views.DeleteCourseView.as_view()),
        name="delete_course",
    ),
    path(
        "offers/<int:course_id>",
        login_required(views.OffersPageView.as_view()),
        name="offers",
    ),
    path(
        "offers/create",
        login_required(views.CreateOfferPageView.as_view()),
        name="create_offer",
    ),
    path(
        "offers/edit/<int:offer_id>",
        login_required(views.EditOfferPageView.as_view()),
        name="edit_offer",
    ),
    path(
        "offers/delete/<int:offer_id>",
        login_required(views.DeleteOfferView.as_view()),
        name="delete_offer",
    ),
    path(
        "offers/details/<int:course_id>/<int:offer_id>",
        login_required(views.OfferDetailsPageView.as_view()),
        name="offer_details",
    ),
    path(
        "offers/remove_student_from_offer/<int:offer_id>/<int:student_id>",
        login_required(views.RemoveStudentFromOfferView.as_view()),
        name="remove_student_from_offer",
    ),
    path(
        "offers/add_student_to_offer/<int:offer_id>",
        login_required(views.AddStudentToOfferView.as_view()),
        name="add_student_to_offer",
    ),
]
