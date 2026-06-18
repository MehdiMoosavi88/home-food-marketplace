from django.urls import path

from .views import (
    ReviewCreateAPIView
)

urlpatterns = [

    path(
        "create/",
        ReviewCreateAPIView.as_view(),
        name="review-create"
    ),

]