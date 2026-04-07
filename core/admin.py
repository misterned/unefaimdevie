from django.contrib import admin

from .models import Advertisement, Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "created_at")
    search_fields = ("title", "body", "category")
    list_filter = ("status", "category", "created_at")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "display_author", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("post__title", "author__username", "author_name", "author_email", "content")

    @admin.display(description="Auteur")
    def display_author(self, obj):
        return obj.display_author


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "merchant", "submitter_label", "price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "merchant", "text")

    @admin.display(description="Soumis par")
    def submitter_label(self, obj):
        return obj.submitter_label
