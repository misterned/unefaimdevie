from .services import user_is_animateur


def role_flags(request):
    user = request.user
    return {"is_animateur": user_is_animateur(user)}
