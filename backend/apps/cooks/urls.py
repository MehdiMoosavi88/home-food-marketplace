from django.urls import path

from .views import (
    CookMeAPIView
)

urlpatterns = [

    path(
        "me/",
        CookMeAPIView.as_view(),
        name="cook-me"
    ),
]