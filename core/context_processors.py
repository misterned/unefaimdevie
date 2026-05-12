from django.conf import settings
from django.db.models import Count

from .models import Post
from .services import user_is_animateur


def role_flags(request):
    user = request.user
    nav_categories = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .exclude(category="")
        .values("category")
        .annotate(count=Count("id"))
        .order_by("-count")
        .values_list("category", flat=True)[:5]
    )
    return {
        "is_animateur": user_is_animateur(user),
        "nav_categories": list(nav_categories),
        "appinsights_connection_string": getattr(settings, "APPLICATIONINSIGHTS_CONNECTION_STRING", ""),
    }
