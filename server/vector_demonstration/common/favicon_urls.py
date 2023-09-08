from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = []

# Only include the favicon urls if we are in a staging or production environment.
# Favicons are not needed in development, and this also prevents errors when running
# tests without having first built the front end app.
if settings.IN_STAGING or settings.IN_PROD or settings.IN_REVIEW:
    urlpatterns += [
        path(
            r"favicon.ico",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/favicon.ico"), permanent=False),
            name="favicon",
        ),
        path(
            r"apple-icon-57x57.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/apple-icon-57x57.png"), permanent=False),
            name="apple-icon-57",
        ),
        path(
            r"apple-icon-60x60.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/apple-icon-60x60.png"), permanent=False),
            name="apple-icon-60",
        ),
        path(
            r"apple-icon-72x72.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/apple-icon-72x72.png"), permanent=False),
            name="apple-icon-72",
        ),
        path(
            r"apple-icon-76x76.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/apple-icon-76x76.png"), permanent=False),
            name="apple-icon-76",
        ),
        path(
            r"apple-icon-114x114.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/apple-icon-114x114.png"), permanent=False),
            name="apple-icon-114",
        ),
        path(
            r"apple-icon-120x120.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/apple-icon-120x120.png"), permanent=False),
            name="apple-icon-120",
        ),
        path(
            r"apple-icon-144x144.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/apple-icon-144x144.png"), permanent=False),
            name="apple-icon-144",
        ),
        path(
            r"apple-icon-152x152.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/apple-icon-152x152.png"), permanent=False),
            name="apple-icon-152",
        ),
        path(
            r"apple-icon-180x180.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/apple-icon-180x180.png"), permanent=False),
            name="apple-icon-180",
        ),
        path(
            r"android-icon-192x192.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/android-icon-192x192.png"), permanent=False),
            name="apple-icon-192",
        ),
        path(
            r"favicon-32x32.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/favicon-32x32.png"), permanent=False),
            name="favicon-32",
        ),
        path(
            r"favicon-96x96.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/favicon-96x96.png"), permanent=False),
            name="favicon-96",
        ),
        path(
            r"favicon-16x16.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/favicon-16x16.png"), permanent=False),
            name="favicon-16",
        ),
        path(
            r"manifest.json",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/manifest.json"), permanent=False),
            name="icon-manifest",
        ),
        path(
            r"ms-icon-144x144.png",
            RedirectView.as_view(url=staticfiles_storage.url("favicons/ms-icon-144x144.png"), permanent=False),
            name="ms-icon",
        ),
    ]
