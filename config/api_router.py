from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from sistema_pei.academics.api.views import EnrollmentDataView
from sistema_pei.core.api.views import SuapTokenValidateView
from sistema_pei.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)

app_name = "api"
urlpatterns = [
    # JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
      "token/suap_token_validate/",
      SuapTokenValidateView.as_view(),
      name="suap_token_validate",
    ),
    path(
      "academics/enrollment_data_update/",
      EnrollmentDataView.as_view(),
      name="enrollment-data-update",
    ),
]
urlpatterns += router.urls
