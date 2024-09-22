from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("~redirect/", view=views.user_redirect_view, name="redirect"),
    path("~update/", view=views.user_update_view, name="update"),
    path("<int:pk>/", view=views.user_detail_view, name="detail"),
    path(
        "users_manage_access/",
        views.UsersManageAccess.as_view(),
        name="users_manage_access",
    ),
]
