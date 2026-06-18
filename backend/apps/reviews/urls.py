from django.urls import path

from .views import (
    ReviewCreateAPIView,
    MyReviewListAPIView,
    PublicCookReviewListAPIView
)

urlpatterns = [

    path(
        "create/",
        ReviewCreateAPIView.as_view(),
        name="review-create"
    ),

    path(
        "my/",
        MyReviewListAPIView.as_view(),
        name="my-reviews"
    ),

    path(
        "public/cooks/<uuid:cook_id>/",
        PublicCookReviewListAPIView.as_view(),
        name="public-cook-reviews"
    ),
]