from django.db import models

from core.models import UUIDBaseModel


class Reservation(UUIDBaseModel):

    customer = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    class Status(models.TextChoices):

        PENDING = (
            "pending",
            "Pending"
        )

        CONFIRMED = (
            "confirmed",
            "Confirmed"
        )

        CANCELLED = (
            "cancelled",
            "Cancelled"
        )

        COMPLETED = (
            "completed",
            "Completed"
        )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    total_price = models.PositiveIntegerField(
        default=0
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return (
            f"{self.customer.username}"
            f" - {self.id}"
        )
    
class ReservationItem(UUIDBaseModel):

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="items"
    )

    menu_item = models.ForeignKey(
        "menus.MenuItem",
        on_delete=models.PROTECT,
        related_name="reservation_items"
    )

    date = models.DateField()

    quantity = models.PositiveIntegerField()

    unit_price = models.PositiveIntegerField()

    class Meta:

        verbose_name = (
            "Reservation Item"
        )

        verbose_name_plural = (
            "Reservation Items"
        )

    def __str__(self):

        return (
            f"{self.menu_item.name}"
            f" x {self.quantity}"
        )
