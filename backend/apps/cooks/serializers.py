from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import CookProfile

from django.db.models import Avg

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
            "average_rating",
            "reviews_count",
            "favorites_count",
        )

    def to_representation(
        self,
        instance
    ):

        data = super().to_representation(
            instance
        )

        if (
            data["average_rating"]
            is not None
        ):
            data["average_rating"] = round(
                float(
                    data["average_rating"]
                ),
                1
            )

        return data
    

class PublicCookSerializer(
    serializers.ModelSerializer
):

    username = serializers.CharField(
        source="user.username"
    )

    class Meta:

        model = CookProfile

        fields = (
            "id",
            "username",
            "city",
            "bio",
            "average_rating",
            "reviews_count",
            "favorites_count",
        )