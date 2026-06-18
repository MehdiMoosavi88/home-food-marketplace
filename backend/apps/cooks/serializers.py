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

    rating = serializers.SerializerMethodField()

    reviews_count = serializers.SerializerMethodField()

    class Meta:

        model = CookProfile

        fields = (
            "id",
            "user",
            "phone",
            "city",
            "address",
            "bio",
            "rating",
            "reviews_count",
        )

    def get_rating(
    self,
    obj
    ):

        result = (
        obj.reviews.aggregate(
            avg=Avg("rating")
        )
        )

        rating = result["avg"]

        if rating is None:
            return 0

        return round(
        rating,
        1
        )


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