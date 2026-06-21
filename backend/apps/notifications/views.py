from rest_framework import generics

from .models import Notification

from .serializers import (
    NotificationSerializer
)

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework import status

from django.shortcuts import get_object_or_404

from django.db.models import Q

class MyNotificationListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        NotificationSerializer
    )

    permission_classes = [
    IsAuthenticated
    ]

    def get_queryset(
        self
    ):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                Notification.objects
                .none()
            )

        return (
            Notification.objects
            .filter(
                Q(
                    user=self.request.user
                )
                |
                Q(
                    is_global=True
                )
            )
            .order_by(
                "-created_at"
            )
        )
    
class NotificationDetailAPIView(
    generics.RetrieveAPIView
):

    serializer_class = (
        NotificationSerializer
    )

    permission_classes = [
    IsAuthenticated
    ]

    def get_queryset(
        self
    ):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                Notification.objects
                .none()
            )

        return (
            Notification.objects
            .filter(
                user=self.request.user
            )
        )
    
class UnreadNotificationCountAPIView(
    APIView
):
    
    permission_classes = [
    IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        count = (
            Notification.objects
            .filter(
                user=request.user,
                is_read=False
            )
            .count()
        )

        return Response(
            {
                "unread_count":
                count
            }
        )
    
    def retrieve(
    self,
    request,
    *args,
    **kwargs
    ):
        instance = self.get_object()

        if not instance.is_read:

            instance.is_read = True

            instance.save(
            update_fields=[
                "is_read"
                ]
                )

        serializer = (
        self.get_serializer(
            instance
        )
    )

        return Response(
        serializer.data
    )
    
class MarkNotificationReadAPIView(
    APIView
):
    
    permission_classes = [
    IsAuthenticated
    ]

    def patch(
        self,
        request,
        pk
    ):

        notification = (
            get_object_or_404(
                Notification,
                pk=pk,
                user=request.user
            )
        )

        if not notification.is_read:

            notification.is_read = True

            notification.save(
                update_fields=[
                    "is_read"
                ]
            )

        return Response(
            {
                "detail":
                "Notification marked as read."
            },
            status=status.HTTP_200_OK
        )
    
class MarkAllNotificationsReadAPIView(
    APIView
):
    
    permission_classes = [
    IsAuthenticated
    ]

    def patch(
        self,
        request
    ):

        updated_count = (
            Notification.objects
            .filter(
                user=request.user,
                is_read=False
            )
            .update(
                is_read=True
            )
        )

        return Response(
            {
                "detail":
                "All notifications marked as read.",
                "updated":
                updated_count
            },
            status=status.HTTP_200_OK
        )
