from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command

from core.models import Comment, Post
from core.services import ensure_animateur_group


class Command(BaseCommand):
    help = "Crée des données de démonstration (animateur, posts, publicités, commentaires)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default="ChangeMe123!",
            help="Mot de passe des comptes de démonstration.",
        )

    def handle(self, *args, **options):
        password = options["password"]
        user_model = get_user_model()

        animateur_group = ensure_animateur_group()

        animateur, _ = user_model.objects.get_or_create(
            username="animateur",
            defaults={"email": "animateur@croisic.local", "is_staff": False},
        )
        animateur.set_password(password)
        animateur.save(update_fields=["password"])
        animateur.groups.add(animateur_group)

        fixture_path = Path("core/fixtures/demo_seed.json")
        if fixture_path.exists():
            call_command("loaddata", str(fixture_path), verbosity=0)
            self.stdout.write(self.style.SUCCESS("Fixture demo_seed.json chargée."))

        post_100 = Post.objects.filter(pk=100).first()
        post_101 = Post.objects.filter(pk=101).first()

        if post_100:
            Comment.objects.get_or_create(
                post=post_100,
                author_name="Marie Le Goff",
                author_email="marie.legoff@example.com",
                content="Très belle initiative pour valoriser la culture locale !",
                defaults={"status": Comment.Status.APPROVED},
            )
            Comment.objects.get_or_create(
                post=post_100,
                author_name="Jean Martin",
                author_email="jean.martin@example.com",
                content="Peut-on proposer un stand lors de l'événement ?",
                defaults={"status": Comment.Status.PENDING},
            )

        if post_101:
            Comment.objects.get_or_create(
                post=post_101,
                author_name="Anne Morvan",
                author_email="anne.morvan@example.com",
                content="Merci pour ces informations patrimoniales.",
                defaults={"status": Comment.Status.APPROVED},
            )

        self.stdout.write(self.style.SUCCESS("Seed terminé avec succès."))
        self.stdout.write(
            "Compte: animateur | mot de passe: "
            f"{password}"
        )
