from django.urls import path

from .views import (
    MyNotificationListAPIView,
    NotificationDetailAPIView,
    UnreadNotificationCountAPIView,
    MarkNotificationReadAPIView,
    MarkAllNotificationsReadAPIView,
)

urlpatterns = [

    path(
        "",
        MyNotificationListAPIView.as_view(),
        name="notification-list"
    ),

    path(
        "<uuid:pk>/",
        NotificationDetailAPIView.as_view(),
        name="notification-detail"
    ),

    path(
        "unread-count/",
        UnreadNotificationCountAPIView.as_view(),
        name="notification-unread-count"
    ),

    path(
        "<uuid:pk>/read/",
        MarkNotificationReadAPIView.as_view(),
        name="notification-read"
    ),

    path(
        "read-all/",
        MarkAllNotificationsReadAPIView.as_view(),
        name="notification-read-all"
    ),
]