from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_nested import routers

from vector_demonstration.common import views as common_views
from vector_demonstration.core import urls as core_urls

router = routers.SimpleRouter()
if settings.DEBUG:
    router = routers.DefaultRouter()

# extend url patterns here
urlpatterns = [*core_urls.urlpatterns]

schema_view = get_schema_view(
    openapi.Info(
        title="Vector Demonstration API",
        default_version="1.0",
        description="Vector Demonstration Docs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@thinknimble.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = urlpatterns + [
    re_path(r"^api/swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path(r"api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path(r"api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path(r"api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path("api-auth/", include("rest_framework.urls"))]

urlpatterns += [
    re_path(r".*", common_views.index),
]
