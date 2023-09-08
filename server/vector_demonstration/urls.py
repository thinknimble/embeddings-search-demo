from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(r"staff/", admin.site.urls),
    path(r"", include("vector_demonstration.common.favicon_urls")),
    path(r"", include("vector_demonstration.common.urls")),
]
