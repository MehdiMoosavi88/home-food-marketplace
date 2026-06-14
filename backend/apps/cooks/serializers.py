from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import CookProfile

class CookProfileSerializer(
    serializers.ModelSerializer
):

    user = UserSerializer(
        read_only=True
    )

    class Meta:

        model = CookProfile

        fields = (
            "id",
            "user",
            "phone",
            "city",
            "address",
            "bio",
        )

class PublicCookSerializer(
    serializers.ModelSerializer
):

    username = (
        serializers.CharField(
            source="user.username"
        )
    )

    class Meta:

        model = CookProfile

        fields = (
            "id",
            "username",
            "city",
            "bio",
        )