# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from sistema_pei.people.views import activate_account, StudentCreateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from sistema_pei.core.views import (
    CoursesPageView,
    CreateCoursesPageView,
    CreateSubjectPageView,
    DeleteCourseView,
    DeleteSubjectView,
    EditCoursePageView,
    EditSubjectPageView,
    HomePageView,
    RemoveStudentFromSubjectView,
    ProfilePageView,
    SubjectsPageView,
    UpdateStudentGradesView,
    UsersPageView,
    EditHistoricPersonalDataView,
    EditPersonalDataView,
    UploadStudentFilesView,
    DeletePersonalFilesView,
)

urlpatterns = [
    path(
        "",
        login_required(HomePageView.as_view()),
        name="home",
    ),
    path(
        "academics/",
        include("sistema_pei.academics.urls", namespace="academics"),
    ),
    path(
        "users/",
        login_required(UsersPageView.as_view()),
        name="users",
    ),
    path(
        "profile/<int:student_id>",
        login_required(ProfilePageView.as_view()),
        name="profile",
    ),
    path(
        "profile/<int:student_id>/edit_personal_data/",
        login_required(EditPersonalDataView.as_view()),
        name="edit_personal_data",
    ),
    path(
        "profile/<int:student_id>/update_student_grades/<int:enrollment_id>",
        login_required(UpdateStudentGradesView.as_view()),
        name="update_student_grades",
    ),
    path(
        "profile/<int:student_id>/edit_historic_data/",
        login_required(EditHistoricPersonalDataView.as_view()),
        name="edit_personal_historic_data",
    ),
    path(
        "profile/<int:student_id>/upload_files/",
        login_required(UploadStudentFilesView.as_view()),
        name="upload_files",
    ),
    path(
        "profile/<int:student_id>/delete_file/",
        login_required(DeletePersonalFilesView.as_view()),
        name="delete_personal_file",
    ),
    path(
        "courses/",
        login_required(CoursesPageView.as_view()),
        name="courses",
    ),
    path(
        "courses/create",
        login_required(CreateCoursesPageView.as_view()),
        name="create_course",
    ),
    path(
        "courses/edit/<int:course_id>",
        login_required(EditCoursePageView.as_view()),
        name="edit_course",
    ),
    path(
        "courses/delete/<int:course_id>",
        login_required(DeleteCourseView.as_view()),
        name="delete_course",
    ),
    path(
        "subjects/delete/<int:subject_id>",
        login_required(DeleteSubjectView.as_view()),
        name="delete_subject",
    ),
    path(
        "subjects/<int:course_id>",
        login_required(SubjectsPageView.as_view()),
        name="subjects",
    ),
    path(
        "subjects/create/<int:course_id>",
        login_required(CreateSubjectPageView.as_view()),
        name="create_subject",
    ),
    path(
        "subjects/edit/<int:subject_id>",
        login_required(EditSubjectPageView.as_view()),
        name="edit_subject",
    ),
    path(
        "subjects/remove_student_from_subject/<int:subject_id>/<int:student_id>",
        login_required(RemoveStudentFromSubjectView.as_view()),
        name="remove_student_from_subject",
    ),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("sistema_pei.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("activate/<uidb64>/<token>/", activate_account, name="activate"),
    path(
        "student/create/",
        login_required(StudentCreateView.as_view()),
        name="student_create",
    ),
    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Reload
    path("__reload__/", include("django_browser_reload.urls")),
    # Your stuff: custom urls includes go here
    # ...
    path("social/", include("social_django.urls", namespace="social")),
    path("suap_backend/", include("suap_backend.urls", namespace="suap_login")),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
