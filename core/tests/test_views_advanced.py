import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from core.models import Post, Advertisement, Comment
from core.services import ensure_animateur_group

@pytest.mark.django_db
def test_home_view_featured_ad():
    ad = Advertisement.objects.create(title="Pub", merchant="M", text="T", price=1, status=Advertisement.Status.APPROVED, featured=True)
    client = Client()
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
    assert b"Pub" in response.content

@pytest.mark.django_db
def test_post_detail_view_with_comment_and_edit():
    user = get_user_model().objects.create(username="author")
    group = ensure_animateur_group()
    user.groups.add(group)
    user.save()
    post = Post.objects.create(title="T", slug="t", author=user, body="B", category="C", status=Post.Status.PUBLISHED)
    comment = Comment.objects.create(post=post, author=user, content="ok", status=Comment.Status.APPROVED)
    client = Client()
    client.force_login(user)
    url = reverse("post-detail", args=[post.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert b"ok" in response.content
    assert b"Modifier l'article" in response.content

@pytest.mark.django_db
def test_post_list_view_only_published():
    user = get_user_model().objects.create(username="author2")
    Post.objects.create(title="T1", slug="t1", author=user, body="B", category="C", status=Post.Status.DRAFT)
    Post.objects.create(title="T2", slug="t2", author=user, body="B", category="C", status=Post.Status.PUBLISHED)
    client = Client()
    url = reverse("post-list")
    response = client.get(url)
    assert b"T2" in response.content
    assert b"T1" not in response.content
