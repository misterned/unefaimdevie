
from django.contrib import admin
from .models_email import EmailSubscriber

# Gestion des abonnés email dans l'admin
@admin.register(EmailSubscriber)
class EmailSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed", "created_at")
    list_filter = ("subscribed", "created_at")
    search_fields = ("email",)
"""
Configuration de l'interface d'administration Django pour les modèles principaux.
"""
from django import forms
from django.contrib import admin

from .forms import QuillWidget
from .models import Advertisement, Comment, Post


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'body': QuillWidget(toolbar='rich'),
        }


class AdvertisementAdminForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = '__all__'
        widgets = {
            'text': QuillWidget(toolbar='simple'),
        }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin pour le modèle Post."""
    form = PostAdminForm
    list_display = ("title", "author", "category", "status", "created_at")
    search_fields = ("title", "body", "category")
    list_filter = ("status", "category", "created_at")
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        """Notifie les abonnés email lors du passage brouillon → publié."""
        import logging
        _log = logging.getLogger(__name__)
        old_status = Post.objects.filter(pk=obj.pk).values_list("status", flat=True).first() if change else None
        super().save_model(request, obj, form, change)
        if obj.status == Post.Status.PUBLISHED and old_status != Post.Status.PUBLISHED:
            try:
                from core.notify import notify_new_post
                notify_new_post(obj)
            except Exception as e:
                _log.error("Erreur notify_new_post (admin) : %s", e, exc_info=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin pour le modèle Comment."""
    list_display = ("post", "display_author", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("post__title", "author__username", "author_name", "author_email", "content")

    @admin.display(description="Auteur")
    def display_author(self, obj):
        """Affiche le nom de l'auteur du commentaire."""
        return obj.display_author


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """Admin pour le modèle Advertisement."""
    form = AdvertisementAdminForm
    list_display = ("title", "merchant", "featured", "status", "price", "created_at")
    list_editable = ["featured", "status"]
    list_filter = ("featured", "status", "created_at")
    search_fields = ("title", "merchant", "text")
