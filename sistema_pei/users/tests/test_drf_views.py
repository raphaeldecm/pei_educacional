import pytest
from rest_framework.test import APIRequestFactory

from sistema_pei.users.api.views import UserViewSet
from sistema_pei.users.models import User


class TestUserViewSet:
    @pytest.fixture()
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore[call-arg, arg-type, misc]

        expected_data = {
            "name": user.name,
        }

        for key, value in expected_data.items():
            assert response.data[key] == value

        assert "url" in response.data
        assert f"/{user.pk}/" in response.data["url"]
