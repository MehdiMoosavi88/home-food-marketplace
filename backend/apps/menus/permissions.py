from rest_framework.permissions import (
    BasePermission
)

class IsMenuOwner(
    BasePermission
):

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):

        return (
            obj.menu.cook.user
            ==
            request.user
        )