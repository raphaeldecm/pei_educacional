from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("~redirect/", view=views.user_redirect_view, name="redirect"),
    path("~update/", view=views.user_update_view, name="update"),
    path("<int:pk>/", view=views.user_detail_view, name="detail"),
    path(
        "list/",
        views.UsersManageAccess.as_view(),
        name="list",
    ),
    path(
        "manage_user/<int:pk>/",
        views.UserManagerUpdate.as_view(),
        name="manage_user",
    ),
]
