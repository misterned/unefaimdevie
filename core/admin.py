"""
Configuration de l'interface d'administration Django pour les modèles principaux.
"""
from django.contrib import admin

from .models import Advertisement, Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin pour le modèle Post."""
    list_display = ("title", "author", "category", "status", "created_at")
    search_fields = ("title", "body", "category")
    list_filter = ("status", "category", "created_at")
    prepopulated_fields = {"slug": ("title",)}


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
    list_display = ("title", "merchant", "featured", "status", "price", "created_at")
    list_editable = ["featured", "status"]
    list_filter = ("featured", "status", "created_at")
    search_fields = ("title", "merchant", "text")
