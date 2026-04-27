from django.contrib.auth.models import Group

ANIMATEUR_GROUP_NAME = "animateur"


def ensure_animateur_group() -> Group:
    group, _ = Group.objects.get_or_create(name=ANIMATEUR_GROUP_NAME)
    return group


def get_user_identifier(user) -> str:
    username_getter = getattr(user, "get_username", None)
    if callable(username_getter):
        username = username_getter()
        if username:
            return username

    username_field = getattr(user, "USERNAME_FIELD", "username")
    username = getattr(user, username_field, "")
    if username:
        return username

    fallback_username = getattr(user, "username", "")
    if fallback_username:
        return fallback_username

    return str(user)


def user_is_admin(user) -> bool:
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def user_is_animateur(user) -> bool:
    return user_is_admin(user) or (
        user.is_authenticated and user.groups.filter(name=ANIMATEUR_GROUP_NAME).exists()
    )


def can_manage_post(user, post) -> bool:
    return user_is_admin(user) or (user_is_animateur(user) and post.author_id == user.id)


def can_moderate_comment(user, comment) -> bool:
    return user_is_admin(user) or (user_is_animateur(user) and comment.post.author_id == user.id)
