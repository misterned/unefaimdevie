from .models import Post
from .services import user_is_animateur


def role_flags(request):
    user = request.user
    nav_categories = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .exclude(category="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )
    return {
        "is_animateur": user_is_animateur(user),
        "nav_categories": list(nav_categories),
    }
