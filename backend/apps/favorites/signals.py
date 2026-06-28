from django.db.models.signals import (
    post_save,
    post_delete,
)

from django.dispatch import (
    receiver
)

from .models import (
    FavoriteCook
)

from .models import (
    FavoriteMenuItem
)

from apps.cooks.services.statistics import (
    update_cook_statistics
)

from apps.menus.services.statistics import (
    update_menu_item_statistics
)


@receiver(
    post_save,
    sender=FavoriteCook
)
def favorite_created(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        update_cook_statistics(
            instance.cook
        )


@receiver(
    post_delete,
    sender=FavoriteCook
)
def favorite_deleted(
    sender,
    instance,
    **kwargs
):

    update_cook_statistics(
        instance.cook
    )

@receiver(
    post_save,
    sender=FavoriteMenuItem
)
def menu_item_favorite_created(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        update_menu_item_statistics(
            instance.menu_item
        )


@receiver(
    post_delete,
    sender=FavoriteMenuItem
)
def menu_item_favorite_deleted(
    sender,
    instance,
    **kwargs
):

    update_menu_item_statistics(
        instance.menu_item
    )