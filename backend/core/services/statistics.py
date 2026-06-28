from apps.cooks.services.statistics import (
    update_cook_statistics,
)

from apps.menus.services.statistics import (
    update_menu_item_statistics,
)

from apps.menus.models import (
    MenuItem,
)


def update_statistics_after_reservation(
    reservation
):
    """
    Refresh all cached statistics affected by a reservation.
    """

    items = (
        reservation.items
        .select_related(
            "menu_item__menu__cook"
        )
    )

    first_item = items.first()

    if first_item is None:
        return

    update_cook_statistics(
        first_item.menu_item.menu.cook
    )

    menu_item_ids = (
        items.values_list(
            "menu_item_id",
            flat=True
        )
        .distinct()
    )

    for menu_item in (
        MenuItem.objects.filter(
            id__in=menu_item_ids
        )
    ):

        update_menu_item_statistics(
            menu_item
        )