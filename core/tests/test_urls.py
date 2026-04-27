from django.urls import resolve, reverse
from core.views import HomeView, PostListView

def test_home_url_resolves():
    path = reverse("home")
    assert resolve(path).func.view_class == HomeView

def test_post_list_url_resolves():
    path = reverse("post-list")
    assert resolve(path).func.view_class == PostListView
