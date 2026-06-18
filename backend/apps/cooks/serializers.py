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

    average_rating = (
        serializers.SerializerMethodField()
    )

    reviews_count = (
        serializers.SerializerMethodField()
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
        )

    def get_average_rating(
        self,
        obj
    ):

        result = (
            obj.reviews.aggregate(
                avg=Avg("rating")
            )
        )

        avg = result["avg"]

        if avg is None:
            return None

        return round(avg, 1)

    def get_reviews_count(
        self,
        obj
    ):

        return (
            obj.reviews.count()
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