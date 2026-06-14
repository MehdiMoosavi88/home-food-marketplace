from django.urls import path

from .views import (
    CookMeAPIView,
    PublicCookListAPIView
)

urlpatterns = [

    path(
        "me/",
        CookMeAPIView.as_view(),
        name="cook-me"
    ),

    path(
    "public/cooks/",
    PublicCookListAPIView.as_view(),
    name="public-cooks"
),
]