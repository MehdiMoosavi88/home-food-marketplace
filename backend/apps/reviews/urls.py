from django.urls import path

from .views import (
    ReviewCreateAPIView,
    MyReviewListAPIView,
    PublicCookReviewListAPIView,

    CommentCreateAPIView,
    CookCommentListAPIView,
    MenuCommentListAPIView,
    MenuItemCommentListAPIView
)

urlpatterns = [

    # Reviews

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

    # Comments

    path(
        "comments/create/",
        CommentCreateAPIView.as_view(),
        name="comment-create"
    ),

    path(
        "comments/cooks/<uuid:cook_id>/",
        CookCommentListAPIView.as_view(),
        name="cook-comments"
    ),

    path(
        "comments/menus/<uuid:menu_id>/",
        MenuCommentListAPIView.as_view(),
        name="menu-comments"
    ),

    path(
        "comments/menu-items/<uuid:menu_item_id>/",
        MenuItemCommentListAPIView.as_view(),
        name="menu-item-comments"
    ),
]