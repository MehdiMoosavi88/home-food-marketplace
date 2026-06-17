from django.db import models

from django.core.exceptions import (
    ValidationError
)

from core.models import UUIDBaseModel


class Review(UUIDBaseModel):

    customer = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    reservation = models.OneToOneField(
        "reservations.Reservation",
        on_delete=models.CASCADE,
        related_name="review"
    )

    cook = models.ForeignKey(
        "cooks.CookProfile",
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField(
        blank=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def clean(self):

        if (
            self.rating < 1
            or
            self.rating > 5
        ):
            raise ValidationError(
                "Rating must be between 1 and 5."
            )

    def __str__(self):

        return (
            f"{self.customer.username}"
            f" - {self.rating}"
        )


class Comment(UUIDBaseModel):

    customer = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    cook = models.ForeignKey(
        "cooks.CookProfile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )

    menu = models.ForeignKey(
        "menus.Menu",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )

    menu_item = models.ForeignKey(
        "menus.MenuItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )

    text = models.TextField()

    is_approved = models.BooleanField(
        default=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def clean(self):

        targets = [
            self.cook,
            self.menu,
            self.menu_item
        ]

        selected = len(
            [
                target
                for target in targets
                if target is not None
            ]
        )

        if selected != 1:

            raise ValidationError(
                "Exactly one target must be selected."
            )

    def __str__(self):

        return (
            self.text[:50]
        )