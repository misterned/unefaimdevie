import pytest
from django.contrib.auth import get_user_model
from core.services import (
    get_user_identifier,
    user_is_admin,
    user_is_animateur,
    can_manage_post,
    can_moderate_comment,
    ensure_animateur_group,
)
from core.models import Post, Comment
from django.contrib.auth.models import Group, AnonymousUser

@pytest.mark.django_db
def test_get_user_identifier_username():
    user = get_user_model().objects.create(username="identuser")
    assert get_user_identifier(user) == "identuser"

@pytest.mark.django_db
def test_user_is_admin_superuser():
    user = get_user_model().objects.create(username="admin", is_superuser=True)
    assert user_is_admin(user)

@pytest.mark.django_db
def test_user_is_animateur_group():
    user = get_user_model().objects.create(username="anim")
    group = ensure_animateur_group()
    user.groups.add(group)
    user.save()
    assert user_is_animateur(user)

@pytest.mark.django_db
def test_can_manage_post():
    user = get_user_model().objects.create(username="author")
    group = ensure_animateur_group()
    user.groups.add(group)
    user.save()
    post = Post.objects.create(title="t", slug="t", author=user, body="b", category="c", status=Post.Status.PUBLISHED)
    assert can_manage_post(user, post)

@pytest.mark.django_db
def test_can_moderate_comment():
    user = get_user_model().objects.create(username="author2")
    group = ensure_animateur_group()
    user.groups.add(group)
    user.save()
    post = Post.objects.create(title="t2", slug="t2", author=user, body="b", category="c", status=Post.Status.PUBLISHED)
    comment = Comment.objects.create(post=post, author=user, content="ok")
    assert can_moderate_comment(user, comment)

def test_user_is_admin_false_for_anonymous():
    user = AnonymousUser()
    assert not user_is_admin(user)
