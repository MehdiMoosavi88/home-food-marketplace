from django.db.models.signals import (
    post_save,
    post_delete,
)

from django.dispatch import (
    receiver
)

from .models import (
    Review
)

from core.services.statistics import (
    update_statistics_after_reservation
)


@receiver(
    post_save,
    sender=Review
)
def review_saved(
    sender,
    instance,
    **kwargs
):

    update_statistics_after_reservation(
        instance.reservation
    )


@receiver(
    post_delete,
    sender=Review
)
def review_deleted(
    sender,
    instance,
    **kwargs
):

    update_statistics_after_reservation(
        instance.reservation
    )