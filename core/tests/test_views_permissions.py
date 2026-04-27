import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from core.models import Post, Comment
from core.services import ensure_animateur_group

@pytest.mark.django_db
def test_post_detail_404():
    client = Client()
    url = reverse("post-detail", args=[99999])
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_update_permission_denied():
    user1 = get_user_model().objects.create(username="user1")
    user2 = get_user_model().objects.create(username="user2")
    group = ensure_animateur_group()
    user1.groups.add(group)
    user1.save()
    post = Post.objects.create(title="T", slug="t", author=user1, body="B", category="C", status=Post.Status.PUBLISHED)
    client = Client()
    client.force_login(user2)
    url = reverse("post-update", args=[post.pk])
    response = client.get(url)
    # Soit 403, soit redirection, selon la vue
    assert response.status_code in (302, 403)

@pytest.mark.django_db
def test_comment_moderation_permission_denied():
    user1 = get_user_model().objects.create(username="user3")
    user2 = get_user_model().objects.create(username="user4")
    group = ensure_animateur_group()
    user1.groups.add(group)
    user1.save()
    post = Post.objects.create(title="T2", slug="t2", author=user1, body="B", category="C", status=Post.Status.PUBLISHED)
    comment = Comment.objects.create(post=post, author=user1, content="ok")
    client = Client()
    client.force_login(user2)
    url = reverse("moderation-comment-action", args=[comment.pk, "approve"])
    response = client.post(url)
    assert response.status_code in (302, 403)
