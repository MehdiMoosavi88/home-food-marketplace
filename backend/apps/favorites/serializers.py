from rest_framework import serializers

from .models import (
    FavoriteCook,
    FavoriteMenuItem
)

class FavoriteCookSerializer(
    serializers.ModelSerializer
):

    cook_name = serializers.CharField(
        source=
        "cook.user.username",
        read_only=True
    )

    class Meta:

        model = FavoriteCook

        fields = (
            "id",
            "cook",
            "cook_name",
            "created_at",
        )

class FavoriteMenuItemSerializer(
    serializers.ModelSerializer
):

    menu_item_name = serializers.CharField(
        source=
        "menu_item.name",
        read_only=True
    )

    class Meta:

        model = FavoriteMenuItem

        fields = (
            "id",
            "menu_item",
            "menu_item_name",
            "created_at",
        )