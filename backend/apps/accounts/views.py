from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import (
    RegisterSerializer,
    UserSerializer
)

@swagger_auto_schema(
    tags=["Authentication"]
)
def post(self, request, *args, **kwargs):
    return super().post(request, *args, **kwargs)

@swagger_auto_schema(
    tags=["Authentication"]
)
class RegisterAPIView(
    generics.CreateAPIView
):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer

    permission_classes = [
        AllowAny
    ]

class MeAPIView(APIView):

    @swagger_auto_schema(
    tags=["Authentication"]
    )
    def get(
        self,
        request
    ):

        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data
        )
