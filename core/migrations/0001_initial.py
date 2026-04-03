from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Advertisement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("merchant", models.CharField(max_length=120)),
                ("image", models.ImageField(blank=True, null=True, upload_to="ads/images/")),
                ("text", models.TextField(max_length=1200)),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "En attente"), ("approved", "Validé"), ("rejected", "Rejeté")],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("validated_at", models.DateTimeField(blank=True, null=True)),
                (
                    "submitted_by",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="advertisements", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150, verbose_name="Titre")),
                ("slug", models.SlugField(max_length=170, unique=True)),
                ("body", models.TextField(verbose_name="Corps")),
                ("image", models.ImageField(blank=True, null=True, upload_to="posts/images/")),
                ("category", models.CharField(max_length=80, verbose_name="Catégorie")),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "Brouillon"), ("published", "Publié")],
                        default="draft",
                        max_length=10,
                    ),
                ),
                (
                    "notebook_html",
                    models.FileField(
                        blank=True,
                        help_text="HTML pré-généré depuis un notebook (nbconvert).",
                        null=True,
                        upload_to="posts/notebooks/",
                    ),
                ),
                ("powerbi_embed_code", models.TextField(blank=True, help_text="Code iframe Power BI")),
                ("video_url", models.URLField(blank=True, help_text="URL YouTube/Vimeo")),
                ("video_file", models.FileField(blank=True, null=True, upload_to="posts/videos/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="posts", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField(max_length=1000)),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "En attente"), ("approved", "Validé"), ("rejected", "Rejeté")],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "post",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="core.post"),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
