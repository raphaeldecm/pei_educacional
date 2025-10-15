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
from django.views.generic.base import RedirectView
from django.views.defaults import page_not_found

from sistema_pei.people.views import activate_account
from sistema_pei.core.views import (
    HomeListView,
)

urlpatterns = [
    path("app/", RedirectView.as_view(url="/peis_sync/app/", permanent=False)),
    path(
        "people/",
        include("sistema_pei.people.urls", namespace="people"),
    ),
    path(
        "",
        login_required(HomeListView.as_view()),
        name="home",
    ),
    path(
        "academics/",
        include("sistema_pei.academics.urls", namespace="academics"),
    ),
    path(
        "educational_plan/",
        include("sistema_pei.educational_plan.urls", namespace="educational_plan"),
    ),
    path(
        "peis_sync/",
        include("sistema_pei.peis_sync.urls", namespace="peis_sync"),
    ),
    path(
        "about/",
        TemplateView.as_view(template_name="about.html"),
        name="about",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("sistema_pei.users.urls", namespace="users")),
    # Rotas de alteração de senha e recuperação (Desativadas)
    path(
        "accounts/password/change/",
        page_not_found,
        kwargs={"exception": Exception("Not Found")},
    ),
    path(
        "accounts/password/reset/",
        page_not_found,
        kwargs={"exception": Exception("Not Found")},
    ),
    path(
        "accounts/password/reset/done/",
        page_not_found,
        kwargs={"exception": Exception("Not Found")},
    ),
    path(
        "accounts/password/reset/key/<uidb36>/<key>/",
        page_not_found,
        kwargs={"exception": Exception("Not Found")},
    ),
    # Allauth (login, logout, signup, etc.)
    path("accounts/", include("allauth.urls")),
    path("activate/<uidb64>/<token>/", activate_account, name="activate"),
    # Reload
    path("__reload__/", include("django_browser_reload.urls")),
    # Your stuff: custom urls includes go here
    # ...
    path("social/", include("social_django.urls", namespace="social")),
    path(
        "suap_backend/",
        include("sistema_pei.suap_backend.urls", namespace="suap_login"),
    ),
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
