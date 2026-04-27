import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from core.models import Post

@pytest.mark.django_db
def test_post_save_slug():
    user = get_user_model().objects.create(username="sluguser")
    post = Post.objects.create(title="Titre spécial !", author=user, body="Texte", category="cat", status=Post.Status.PUBLISHED)
    assert post.slug == "titre-special"

@pytest.mark.django_db
def test_post_clean_video_file_validation():
    user = get_user_model().objects.create(username="videouser")
    post = Post(title="Titre", author=user, body="Texte", category="cat", status=Post.Status.PUBLISHED)
    class DummyFileObj:
        content_type = "image/png"
    class DummyFieldFile:
        file = DummyFileObj()
    post.video_file = DummyFieldFile()
    with pytest.raises(ValidationError):
        post.clean()

@pytest.mark.django_db
def test_post_get_absolute_url():
    user = get_user_model().objects.create(username="absurluser")
    post = Post.objects.create(title="Titre", author=user, body="Texte", category="cat", status=Post.Status.PUBLISHED)
    assert post.get_absolute_url() == f"/post/{post.pk}/"
