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
    list_display = ("post", "author", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("post__title", "author__username", "content")


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "merchant", "price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "merchant", "text")
