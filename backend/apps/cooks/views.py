from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import CookProfile

from .serializers import (
    CookProfileSerializer
)

from .permissions import (
    IsCook
)

from drf_yasg.utils import (
    swagger_auto_schema
)

class CookMeAPIView(
    generics.RetrieveUpdateAPIView
):

    serializer_class = (
        CookProfileSerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_object(self):
        return self.request.user.cook_profile

    @swagger_auto_schema(
        tags=["Cook Profile"]
    )
    def get(
        self,
        request,
        *args,
        **kwargs
    ):
        return super().get(
            request,
            *args,
            **kwargs
        )

    @swagger_auto_schema(
        tags=["Cook Profile"]
    )
    def patch(
        self,
        request,
        *args,
        **kwargs
    ):
        return super().patch(
            request,
            *args,
            **kwargs
        )
    
class PublicCookListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        CookProfileSerializer
    )

    permission_classes = [AllowAny]

    queryset = (
        CookProfile.objects
        .select_related("user")
        .order_by(
            "user__username"
        )
    )