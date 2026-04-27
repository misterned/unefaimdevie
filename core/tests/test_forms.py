import pytest
from core.forms import PostForm, CommentForm
from core.models import Post
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_post_form_valid():
    user = get_user_model().objects.create(username="formuser")
    form = PostForm(data={
        "title": "Titre court",
        "slug": "titre-court",
        "body": "Texte",
        "category": "cat",
        "status": Post.Status.PUBLISHED,
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_post_form_title_too_long():
    user = get_user_model().objects.create(username="formuser2")
    form = PostForm(data={
        "title": "T" * 151,
        "slug": "slug",
        "body": "Texte",
        "category": "cat",
        "status": Post.Status.PUBLISHED,
    })
    assert not form.is_valid()
    assert "title" in form.errors


def test_comment_form_email_optional():
    form = CommentForm(data={"author_name": "A", "content": "B"})
    assert form.is_valid()
