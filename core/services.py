from django.contrib.auth.models import Group


ANIMATEUR_GROUP_NAME = "animateur"


def ensure_animateur_group() -> Group:
    group, _ = Group.objects.get_or_create(name=ANIMATEUR_GROUP_NAME)
    return group
