from math import ceil

from rest_framework.pagination import (
    PageNumberPagination
)

from rest_framework.response import (
    Response
)


class StandardResultsSetPagination(
    PageNumberPagination
):

    page_size = 10

    page_size_query_param = (
        "page_size"
    )

    max_page_size = 100

    page_query_param = (
        "page"
    )

    def get_paginated_response(
        self,
        data
    ):

        page_size = (
            self.get_page_size(
                self.request
            )
        )

        return Response(
            {
                "count":
                self.page.paginator.count,

                "total_pages":
                ceil(
                    self.page.paginator.count
                    /
                    page_size
                ),

                "current_page":
                self.page.number,

                "page_size":
                page_size,

                "next":
                self.get_next_link(),

                "previous":
                self.get_previous_link(),

                "has_next":
                self.page.has_next(),

                "has_previous":
                self.page.has_previous(),

                "results":
                data,
            }
        )