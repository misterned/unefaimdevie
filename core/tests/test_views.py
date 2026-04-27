import pytest
from django.urls import reverse
from django.test import Client
from core.models import Post
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_home_view_status_code():
    client = Client()
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_list_view_status_code():
    client = Client()
    url = reverse("post-list")
    response = client.get(url)
    assert response.status_code == 200
