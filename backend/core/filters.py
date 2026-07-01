from rest_framework.filters import (
    OrderingFilter
)

import django_filters

from apps.cooks.models import CookProfile

from apps.menus.models import MenuItem


class MenuItemOrderingFilter(OrderingFilter):

    ordering_description = (
        "Use the 'ordering' parameter.\n\n"
        "Examples:\n"
        "- ordering=name\n"
        "- ordering=-name\n"
        "- ordering=price\n"
        "- ordering=-price\n"
        "- ordering=rate\n"
        "- ordering=-rate (cook average rating)\n"
        "- ordering=created_at\n"
        "- ordering=-created_at\n\n"
        "Prefix with '-' for descending order."
    )

    ORDERING_MAP = {
    "name": "name",
    "price": "price",
    "favorites": "favorites_count",
    "orders": "orders_count",
    "rate": "menu__cook__average_rating",
    "newest": "created_at",
    }

    def remove_invalid_fields(
        self,
        queryset,
        fields,
        view,
        request,
    ):

        mapped = []

        for field in fields:

            descending = field.startswith("-")

            key = field[1:] if descending else field

            key = self.ORDERING_MAP.get(
                key,
                key,
            )

            if descending:
                key = f"-{key}"

            mapped.append(key)

        return super().remove_invalid_fields(
            queryset,
            mapped,
            view,
            request,
        )

class CookOrderingFilter(
    OrderingFilter
):

    ordering_description = (
        "Use the 'ordering' parameter.\n\n"
        "Examples:\n"
        "- ordering=favorites_count\n"
        "- ordering=-favorites_count\n"
        "- ordering=average_rating\n"
        "- ordering=-average_rating\n"
        "- ordering=reviews_count\n"
        "- ordering=-reviews_count\n"
        "- ordering=created_at\n"
        "- ordering=-created_at\n\n"

        "Prefix with '-' for descending order."
    )

class CookProfileFilter(
    django_filters.FilterSet
):

    city = django_filters.CharFilter(
        lookup_expr="icontains"
    )

    min_rating = (
        django_filters.NumberFilter(
            field_name=
            "average_rating",
            lookup_expr="gte"
        )
    )

    class Meta:

        model = CookProfile

        fields = [
            "city",
            "min_rating",
        ]

class MenuItemFilter(
    django_filters.FilterSet
):

    min_price = (
        django_filters.NumberFilter(
            field_name="price",
            lookup_expr="gte"
        )
    )

    max_price = (
        django_filters.NumberFilter(
            field_name="price",
            lookup_expr="lte"
        )
    )

    is_active = (
    django_filters.BooleanFilter()
    )

    class Meta:

        model = MenuItem

        fields = [
            "min_price",
            "max_price",
            "is_active",
        ]