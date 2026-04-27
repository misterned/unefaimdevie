import pytest
from core.models import Post
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_post_str():
    user = get_user_model().objects.create(username="testuser")
    post = Post.objects.create(title="Titre", slug="titre", author=user, body="Texte", category="cat", status=Post.Status.PUBLISHED)
    assert str(post) == "Titre"
