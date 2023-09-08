from unittest import mock

import pytest
from django.contrib.auth import authenticate
from django.test import Client, override_settings
from pytest_factoryboy import register
from rest_framework.response import Response

from .factories import UserFactory
from .models import User
from .serializers import UserLoginSerializer
from .views import PreviewTemplateView

JSON_RQST_HEADERS = dict(
    content_type="application/json",
    HTTP_ACCEPT="application/json",
)

register(UserFactory)


@pytest.fixture
def test_user():
    user = UserFactory()
    user.save()
    return user


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(email="test@example.com", password="password", first_name="Leslie", last_name="Burke")

    assert user.email == "test@example.com"
    assert user.password
    assert user.password != "password", "Password is stored as plain text"
    assert user.first_name == "Leslie"
    assert user.last_name == "Burke"

    # Validate default permissions
    assert user.is_active

    # AbstractBaseModel
    assert user.id
    assert user.datetime_created
    assert user.last_edited

    # PermissionsMixin
    assert hasattr(user, "is_superuser")
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_superuser():
    superuser = User.objects.create_superuser(email="test@example.com", password="password", first_name="Leslie", last_name="Burke")

    assert superuser.is_superuser
    assert superuser.last_name == "Burke"


@pytest.mark.django_db
def test_create_user_from_factory(test_user):
    assert test_user.email


@pytest.mark.django_db
def test_user_can_login(test_user):
    test_user.set_password("testing123")
    test_user.save()
    client = Client()
    res = client.post("/api/login/", {"email": test_user.email, "password": "testing123"}, **JSON_RQST_HEADERS)
    assert res.status_code == 200


@pytest.mark.django_db
def test_password_reset(test_user, client):
    test_user.set_password("testing123")
    test_user.save()
    context = test_user.reset_password_context()
    password_reset_url = f"/api/password/reset/confirm/{ context['user'].id }/{ context['token'] }/"
    response = client.post(password_reset_url, data={"password": "new_password"}, format="json")
    assert response.status_code == 200

    # New Password should now work for authentication
    serializer = UserLoginSerializer(data={"email": test_user.email, "password": "new_password"})
    serializer.is_valid()
    assert authenticate(**serializer.validated_data)


@pytest.mark.django_db
def test_user_token_gets_created_from_signal(test_user):
    assert test_user.auth_token


@pytest.mark.django_db
class TestPreviewTemplateView:
    url = "/api/template_preview/"

    @override_settings(DEBUG=False)
    def test_disabled_if_not_debug(self, client):
        response = client.post(self.url)
        assert response.status_code == 404

    @override_settings(DEBUG=True)
    def test_enabled_if_debug(self, client):
        with mock.patch("vector_demonstration.core.views.render", return_value=Response()) as mocked_render:
            client.post(f"{self.url}?template=core/index-placeholder.html")
        assert mocked_render.call_count == 1

    @override_settings(DEBUG=True)
    def test_no_template_provided(self, client):
        response = client.post(self.url)
        assert response.status_code == 400
        assert any("Invalid template name" in e for e in response.json())

    @override_settings(DEBUG=True)
    def test_invalid_template_provided(self, client):
        response = client.post(f"{self.url}?template=SOME_TEMPLATE/WHICH_DOES_NOT/EXIST")
        assert response.status_code == 400
        assert any("Invalid template name" in e for e in response.json())

    def test_parse_value_without_model(self):
        assert PreviewTemplateView.parse_value("some_key", "value") == ("some_key", "value")
        # This is expected behaviour since the nested keys are handled previously by the fill_context_from_params method
        assert PreviewTemplateView.parse_value("some__key", "value") == ("some__key", "value")

    def test_parse_value_with_model(self):
        with mock.patch("vector_demonstration.core.views.apps") as mock_apps:
            PreviewTemplateView.parse_value("some_key:from_model", "core.User:PK")
            assert mock_apps.get_model.call_count == 1
            assert mock_apps.get_model.call_args[0][0] == "core.User"
            assert mock_apps.get_model().objects.get.call_count == 1
            assert mock_apps.get_model().objects.get.call_args.kwargs["pk"] == "PK"

    def test_fill_context_from_params(self):
        context = {}
        PreviewTemplateView().fill_context_from_params(
            context, {"key": 0, "parent__child": 1, "parent__other_child": 2, "parent__multi_nested__child": 3, "parent_field": 4}
        )
        assert context["key"] == 0
        assert context["parent"] == {"child": 1, "other_child": 2, "multi_nested": {"child": 3}}
        assert context["parent_field"] == 4
