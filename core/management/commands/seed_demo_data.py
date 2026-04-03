from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import BaseCommand, call_command

from core.models import Comment, Post


class Command(BaseCommand):
    help = "Crée des données de démonstration (rôles, utilisateurs, posts, ads, commentaires)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default="ChangeMe123!",
            help="Mot de passe des comptes de démonstration.",
        )

    def handle(self, *args, **options):
        password = options["password"]
        user_model = get_user_model()

        animateur_group, _ = Group.objects.get_or_create(name="animateur")

        animateur, _ = user_model.objects.get_or_create(
            username="animateur",
            defaults={"email": "animateur@croisic.local", "is_staff": False},
        )
        animateur.set_password(password)
        animateur.save(update_fields=["password"])
        animateur.groups.add(animateur_group)

        utilisateur, _ = user_model.objects.get_or_create(
            username="lecteur",
            defaults={"email": "lecteur@croisic.local", "is_staff": False},
        )
        utilisateur.set_password(password)
        utilisateur.save(update_fields=["password"])

        commercant, _ = user_model.objects.get_or_create(
            username="commercant",
            defaults={"email": "commercant@croisic.local", "is_staff": False},
        )
        commercant.set_password(password)
        commercant.save(update_fields=["password"])

        fixture_path = Path("core/fixtures/demo_seed.json")
        if fixture_path.exists():
            call_command("loaddata", str(fixture_path), verbosity=0)
            self.stdout.write(self.style.SUCCESS("Fixture demo_seed.json chargée."))

        post_100 = Post.objects.filter(pk=100).first()
        post_101 = Post.objects.filter(pk=101).first()

        if post_100:
            Comment.objects.get_or_create(
                post=post_100,
                author=utilisateur,
                content="Très belle initiative pour valoriser la culture locale !",
                defaults={"status": Comment.Status.APPROVED},
            )
            Comment.objects.get_or_create(
                post=post_100,
                author=commercant,
                content="Peut-on proposer un stand lors de l'événement ?",
                defaults={"status": Comment.Status.PENDING},
            )

        if post_101:
            Comment.objects.get_or_create(
                post=post_101,
                author=utilisateur,
                content="Merci pour ces informations patrimoniales.",
                defaults={"status": Comment.Status.APPROVED},
            )

        self.stdout.write(self.style.SUCCESS("Seed terminé avec succès."))
        self.stdout.write(
            "Comptes: animateur, lecteur, commercant | mot de passe: "
            f"{password}"
        )
