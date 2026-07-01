from django.conf import settings
from django.db import models

from core.models import UUIDBaseModel

from rest_framework.exceptions import (
    ValidationError,
)


class Payment(UUIDBaseModel):

    class Status(models.TextChoices):

        PENDING = (
            "pending",
            "Pending",
        )

        SUCCESS = (
            "success",
            "Success",
        )

        FAILED = (
            "failed",
            "Failed",
        )

        CANCELLED = (
            "cancelled",
            "Cancelled",
        )

    class Gateway(models.TextChoices):

        FAKE = (
            "fake",
            "Fake",
        )

        ZARINPAL = (
            "zarinpal",
            "ZarinPal",
        )

    reservation = models.OneToOneField(
        "reservations.Reservation",
        on_delete=models.CASCADE,
        related_name="payment",
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    gateway = models.CharField(
        max_length=20,
        choices=Gateway.choices,
        default=Gateway.FAKE,
    )

    authority = models.CharField(
        max_length=120,
        blank=True,
    )

    ref_id = models.CharField(
        max_length=120,
        blank=True,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return (
            f"{self.customer.username} - "
            f"{self.amount} - "
            f"{self.status}"
        )
    
    def clean(self):
        if (
        self.__class__.objects.filter(
            reservation=self.reservation,
        )
        .exclude(pk=self.pk)
        .exists()
        ):
            raise ValidationError(
            "A payment already exists for this reservation."
            )
