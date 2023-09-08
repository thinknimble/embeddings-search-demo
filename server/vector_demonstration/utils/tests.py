import pytest

from vector_demonstration.utils.emails import get_html_body
from vector_demonstration.utils.sites import get_site_url


@pytest.mark.parametrize(
    "custom_settings,expected_output",
    [
        ({"CURRENT_DOMAIN": "localhost", "CURRENT_PORT": 8080, "IN_DEV": True}, "http://localhost:8080"),
        ({"CURRENT_DOMAIN": "localhost.com", "CURRENT_PORT": None, "IN_DEV": True}, "http://localhost.com"),
        ({"CURRENT_DOMAIN": "http://localhost/", "CURRENT_PORT": None, "IN_DEV": False}, "https://localhost"),
    ],
)
def test_get_site_url(settings, custom_settings, expected_output):
    for key in custom_settings:
        settings.__setattr__(key, custom_settings[key])
    site_url = get_site_url()
    assert site_url == expected_output


@pytest.mark.parametrize(
    "custom_settings",
    [
        ({"CURRENT_DOMAIN": None, "CURRENT_PORT": 8080, "IN_DEV": True}),
        ({"CURRENT_DOMAIN": "", "CURRENT_PORT": None, "IN_DEV": False}),
    ],
)
def test_get_site_url_negative(settings, custom_settings):
    for key in custom_settings:
        settings.__setattr__(key, custom_settings[key])
    with pytest.raises(Exception):
        get_site_url()


def test_password_reset_email_link(user):
    context = user.reset_password_context()
    html_body = get_html_body("registration/password_reset.html", context)
    assert f"{ context['site_url'] }/password/reset/confirm/{ context['user'].id }/{ context['token'] }" in html_body
