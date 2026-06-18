from django.contrib import admin
from django.db.models import Avg

from .models import (
    CookProfile
)


@admin.register(
    CookProfile
)
class CookProfileAdmin(
    admin.ModelAdmin
):

    list_display = (
        "user",
        "city",
        "phone",
        "average_rating",
    )

    search_fields = (
        "user__username",
        "city",
        "phone",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    def average_rating(
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
            return "-"

        return round(avg, 2)

    average_rating.short_description = (
        "Rating"
    )