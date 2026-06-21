from django.db import models

from core.models import UUIDBaseModel

from django.core.exceptions import ValidationError


class Notification(UUIDBaseModel):

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    is_global = models.BooleanField(
        default=False
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        if self.is_global:
            return (
                f"[GLOBAL] {self.title}"
            )

        if self.user:
            return (
                f"{self.user.username}"
                f" - {self.title}"
            )

        return self.title
    
    def clean(self):

        if self.is_global and self.user:

            raise ValidationError(
            "Global notification must not have a user."
        )

        if not self.is_global and not self.user:

            raise ValidationError(
            "User notification requires a user."
        )