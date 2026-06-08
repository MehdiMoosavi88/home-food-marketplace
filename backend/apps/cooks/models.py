from django.conf import settings
from django.db import models

from core.models import UUIDBaseModel

class CookProfile(UUIDBaseModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cook_profile"
    )

    bio = models.TextField(
        blank=True
    )

    phone = models.CharField(
        max_length=30
    )

    city = models.CharField(
        max_length=100
    )

    address = models.TextField()

    avatar = models.ImageField(
        upload_to="cooks/",
        blank=True,
        null=True
    )

    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Cook Profile"
        verbose_name_plural = "Cook Profiles"

    def __str__(self):
        return self.user.username
