def ensure_animateur_group() -> Group:
"""
Services liés aux permissions et groupes utilisateurs pour l'application.
"""
from django.contrib.auth.models import Group

ANIMATEUR_GROUP_NAME = "animateur"


def ensure_animateur_group() -> Group:
    """Crée ou récupère le groupe 'animateur'.
    
    Returns:
        Group: Le groupe animateur.
    """
    group, _ = Group.objects.get_or_create(name=ANIMATEUR_GROUP_NAME)
    return group


def get_user_identifier(user) -> str:
    """Retourne l'identifiant unique d'un utilisateur (username ou fallback).

    Args:
        user: L'utilisateur à identifier.
    Returns:
        str: L'identifiant unique.
    """
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
    """Vérifie si l'utilisateur est admin (staff ou superuser).

    Args:
        user: L'utilisateur à tester.
    Returns:
        bool: True si admin, sinon False.
    """
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def user_is_animateur(user) -> bool:
    """Vérifie si l'utilisateur est animateur (ou admin).

    Args:
        user: L'utilisateur à tester.
    Returns:
        bool: True si animateur ou admin, sinon False.
    """
    return user_is_admin(user) or (
        user.is_authenticated and user.groups.filter(name=ANIMATEUR_GROUP_NAME).exists()
    )


def can_manage_post(user, post) -> bool:
    """Vérifie si l'utilisateur peut gérer un post.

    Args:
        user: L'utilisateur à tester.
        post: Le post concerné.
    Returns:
        bool: True si gestion possible, sinon False.
    """
    return user_is_admin(user) or (user_is_animateur(user) and post.author_id == user.id)


def can_moderate_comment(user, comment) -> bool:
    """Vérifie si l'utilisateur peut modérer un commentaire.

    Args:
        user: L'utilisateur à tester.
        comment: Le commentaire concerné.
    Returns:
        bool: True si modération possible, sinon False.
    """
    return user_is_admin(user) or (user_is_animateur(user) and comment.post.author_id == user.id)
