from rest_framework.permissions import BasePermission

from apps.accounts.models import User

class IsCook(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
            and
            request.user.role == User.Roles.COOK
        )