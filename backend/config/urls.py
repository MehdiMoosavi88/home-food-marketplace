from django.contrib import admin
from django.urls import (
    path,
    include
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Home Food Marketplace API",
        default_version="v1",
        description="API Documentation for Home Food Marketplace",
        contact=openapi.Contact(
            email="admin@example.com"
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        "api/auth/",
        include(
            "apps.accounts.urls"
        )
    ),

    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),

    path(
        "api/docs/",
        schema_view.with_ui(
            "swagger",
            cache_timeout=0
        ),
        name="swagger-ui"
    ),

    path(
        "api/redoc/",
        schema_view.with_ui(
            "redoc",
            cache_timeout=0
        ),
        name="redoc"
    ),

    path(
    "api/cooks/",
    include(
        "apps.cooks.urls"
    )
),
]