from django.db.models import (
    Avg,
    Count,
)

from apps.reviews.models import (
    Review
)

from apps.favorites.models import (
    FavoriteCook
)


def update_cook_statistics(
    cook
):
    """
    Update all cached statistics
    for a cook.
    """

    review_stats = (
        Review.objects
        .filter(
            cook=cook
        )
        .aggregate(
            average_rating=Avg(
                "rating"
            ),
            reviews_count=Count(
                "id"
            ),
        )
    )

    favorites_count = (
        FavoriteCook.objects
        .filter(
            cook=cook
        )
        .count()
    )

    cook.average_rating = (
        review_stats[
            "average_rating"
        ]
    )

    cook.reviews_count = (
        review_stats[
            "reviews_count"
        ]
    )

    cook.favorites_count = (
        favorites_count
    )

    cook.save(
        update_fields=[
            "average_rating",
            "reviews_count",
            "favorites_count",
        ]
    )