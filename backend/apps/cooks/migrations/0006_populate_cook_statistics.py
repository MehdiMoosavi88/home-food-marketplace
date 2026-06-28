from django.db import migrations
from django.db.models import Avg, Count


def populate_cook_statistics(apps, schema_editor):

    CookProfile = apps.get_model(
        "cooks",
        "CookProfile"
    )

    Review = apps.get_model(
        "reviews",
        "Review"
    )

    FavoriteCook = apps.get_model(
        "favorites",
        "FavoriteCook"
    )

    for cook in CookProfile.objects.all():

        review_stats = (
            Review.objects
            .filter(cook_id=cook.id)
            .aggregate(
                average_rating=Avg("rating"),
                reviews_count=Count("id"),
            )
        )

        cook.average_rating = review_stats["average_rating"]
        cook.reviews_count = review_stats["reviews_count"]

        cook.favorites_count = (
            FavoriteCook.objects
            .filter(cook_id=cook.id)
            .count()
        )

        cook.save(
            update_fields=[
                "average_rating",
                "reviews_count",
                "favorites_count",
            ]
        )


def reverse_populate_cook_statistics(
    apps,
    schema_editor
):

    CookProfile = apps.get_model(
        "cooks",
        "CookProfile"
    )

    CookProfile.objects.update(
        average_rating=None,
        reviews_count=0,
        favorites_count=0,
    )


class Migration(migrations.Migration):

    dependencies = [
        (
            "cooks",
            "0005_cookprofile_favorites_count",
        ),
        (
            "reviews",
            "0002_rename_is_approved_comment_is_active",
        ),
        (
            "favorites",
            "0001_initial",
        ),
    ]

    operations = [
        migrations.RunPython(
            populate_cook_statistics,
            reverse_populate_cook_statistics,
        ),
    ]