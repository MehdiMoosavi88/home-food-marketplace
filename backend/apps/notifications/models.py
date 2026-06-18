from django.db import models

from core.models import UUIDBaseModel


class Notification(
    UUIDBaseModel
):

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(
        self
    ):
        return (
            f"{self.user.username}"
            f" - {self.title}"
        )
