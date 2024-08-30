from django.urls import path
from django.contrib.auth.decorators import login_required

from sistema_pei.academics.views import AddStudentToOfferView, CreateOfferPageView, DeleteOfferView, EditOfferPageView, OfferDetailsPageView, OffersPageView, RemoveStudentFromOfferView

app_name = "academics"
urlpatterns = [
    path(
        "offers/<int:course_id>",
        login_required(OffersPageView.as_view()),
        name="offers",
    ),
    path(
        "offers/create",
        login_required(CreateOfferPageView.as_view()),
        name="create_offer",
    ),
    path(
        "offers/edit/<int:offer_id>",
        login_required(EditOfferPageView.as_view()),
        name="edit_offer",
    ),
    path(
        "offers/delete/<int:offer_id>",
        login_required(DeleteOfferView.as_view()),
        name="delete_offer",
    ),
    path(
        "offers/details/<int:course_id>/<int:offer_id>",
        login_required(OfferDetailsPageView.as_view()),
        name="offer_details",
    ),
    path(
        "offers/remove_student_from_offer/<int:offer_id>/<int:student_id>",
        login_required(RemoveStudentFromOfferView.as_view()),
        name="remove_student_from_offer",
    ),
    path(
        "offers/add_student_to_offer/<int:offer_id>",
        login_required(AddStudentToOfferView.as_view()),
        name="add_student_to_offer",
    ),
]