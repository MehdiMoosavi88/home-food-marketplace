from django.db.models import Avg

from apps.reservations.models import (
    Reservation,
    ReservationItem,
)

from apps.favorites.models import (
    FavoriteMenuItem,
)


def update_menu_item_statistics(menu_item):

    menu_item.orders_count = (
        ReservationItem.objects.filter(
            menu_item=menu_item,
            reservation__status__in=Reservation.ACTIVE_STATUSES,
        ).count()
    )

    menu_item.favorites_count = (
        FavoriteMenuItem.objects.filter(
            menu_item=menu_item
        ).count()
    )

    menu_item.save(
        update_fields=[
            "orders_count",
            "favorites_count",
        ]
    )