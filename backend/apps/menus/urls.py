from django.urls import path

from .views import (
    CookMenuAPIView
)

urlpatterns = [

    path(
        "me/",
        CookMenuAPIView.as_view(),
        name="cook-menu"
    ),
]