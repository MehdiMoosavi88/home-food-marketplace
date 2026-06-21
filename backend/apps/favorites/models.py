from django.db import models

from core.models import UUIDBaseModel


class FavoriteCook(UUIDBaseModel):

    customer = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="favorite_cooks"
    )

    cook = models.ForeignKey(
        "cooks.CookProfile",
        on_delete=models.CASCADE,
        related_name="followers"
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "customer",
                    "cook"
                ],
                name="unique_customer_cook_favorite"
            )
        ]

    def __str__(self):

        return (
            f"{self.customer.username}"
            f" -> "
            f"{self.cook.user.username}"
        )


class FavoriteMenuItem(UUIDBaseModel):

    customer = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="favorite_menu_items"
    )

    menu_item = models.ForeignKey(
        "menus.MenuItem",
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "customer",
                    "menu_item"
                ],
                name="unique_customer_menuitem_favorite"
            )
        ]

    def __str__(self):

        return (
            f"{self.customer.username}"
            f" -> "
            f"{self.menu_item.name}"
        )
