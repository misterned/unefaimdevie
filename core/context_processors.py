def role_flags(request):
    user = request.user
    is_animateur = False
    if user.is_authenticated:
        is_animateur = user.is_superuser or user.is_staff or user.groups.filter(name="animateur").exists()
    return {"is_animateur": is_animateur}
