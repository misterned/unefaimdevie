from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Brouillon"
        PUBLISHED = "published", "Publié"

    title = models.CharField("Titre", max_length=150)
    slug = models.SlugField(unique=True, max_length=170)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    body = models.TextField("Corps")
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
    category = models.CharField("Catégorie", max_length=80)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    notebook_html = models.FileField(
        upload_to="posts/notebooks/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["html", "htm"])],
        help_text="HTML pré-généré depuis un notebook (nbconvert).",
    )
    powerbi_embed_code = models.TextField(blank=True, help_text="Code iframe Power BI")
    video_url = models.URLField(blank=True, help_text="URL YouTube/Vimeo")
    video_file = models.FileField(
        upload_to="posts/videos/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["mp4", "webm", "ogg"])],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.video_file and hasattr(self.video_file, "file"):
            content_type = getattr(self.video_file.file, "content_type", "")
            if content_type and not content_type.startswith("video/"):
                raise ValidationError({"video_file": "Le fichier doit être un média vidéo valide."})

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        APPROVED = "approved", "Validé"
        REJECTED = "rejected", "Rejeté"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=1000)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commentaire de {self.author} sur {self.post}"


class Advertisement(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        APPROVED = "approved", "Validé"
        REJECTED = "rejected", "Rejeté"

    title = models.CharField(max_length=150)
    merchant = models.CharField(max_length=120)
    image = models.ImageField(upload_to="ads/images/", blank=True, null=True)
    text = models.TextField(max_length=1200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="advertisements",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.merchant})"
