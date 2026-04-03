from django.urls import path

from .views import (
    AdvertisementCreateView,
    AdvertisementListView,
    AdvertisementModerationActionView,
    AdvertisementModerationListView,
    CommentCreateView,
    CommentModerationActionView,
    CommentModerationListView,
    PostCreateView,
    PostDetailView,
    PostListView,
    PostUpdateView,
)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/comment/", CommentCreateView.as_view(), name="post-comment"),
    path("moderation/comments/", CommentModerationListView.as_view(), name="moderation-comments"),
    path(
        "moderation/comments/<int:pk>/<str:action>/",
        CommentModerationActionView.as_view(),
        name="moderation-comment-action",
    ),
    path("ads/", AdvertisementListView.as_view(), name="ad-list"),
    path("ads/submit/", AdvertisementCreateView.as_view(), name="ad-submit"),
    path("moderation/ads/", AdvertisementModerationListView.as_view(), name="moderation-ads"),
    path(
        "moderation/ads/<int:pk>/<str:action>/",
        AdvertisementModerationActionView.as_view(),
        name="moderation-ad-action",
    ),
]
