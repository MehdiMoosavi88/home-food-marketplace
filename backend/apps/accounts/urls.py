from django.urls import path

from .views import (
    RegisterAPIView,
    MeAPIView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path(
        "register/",
        RegisterAPIView.as_view()
    ),

    path(
        "me/",
        MeAPIView.as_view()
    ),

    path(
    "login/",
    TokenObtainPairView.as_view()
    ),

    path(
    "token/refresh/",
    TokenRefreshView.as_view()
    ),
]