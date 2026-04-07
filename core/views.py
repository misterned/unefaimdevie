from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AdvertisementForm, CommentForm, PostForm
from .models import Advertisement, Comment, Post
from .services import (
    can_manage_post,
    can_moderate_comment,
    get_user_identifier,
    user_is_admin,
    user_is_animateur,
)


class AnimateurRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return user_is_animateur(self.request.user)


class HomeView(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(status=Comment.Status.APPROVED)
        context["can_edit_post"] = can_manage_post(self.request.user, self.object)
        return context


class PostCreateView(AnimateurRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "posts/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Article créé avec succès.")
        return super().form_valid(form)


class PostUpdateView(AnimateurRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = "posts/post_form.html"

    def test_func(self):
        return can_manage_post(self.request.user, self.get_object())

    def form_valid(self, form):
        messages.success(self.request, "Article modifié avec succès.")
        return super().form_valid(form)


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Post, pk=self.kwargs["pk"], status=Post.Status.PUBLISHED)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.article
        return context

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.setdefault("author_name", get_user_identifier(self.request.user))
            initial.setdefault("author_email", self.request.user.email)
        return initial

    def form_valid(self, form):
        form.instance.post = self.article
        form.instance.status = Comment.Status.PENDING
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
            form.instance.author_name = form.cleaned_data["author_name"] or get_user_identifier(self.request.user)
            form.instance.author_email = form.cleaned_data["author_email"] or self.request.user.email
        messages.info(
            self.request,
            "Commentaire soumis. Il sera publié après validation par un modérateur.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.article.get_absolute_url()


class CommentModerationListView(AnimateurRequiredMixin, ListView):
    model = Comment
    template_name = "posts/moderation_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        queryset = Comment.objects.filter(status=Comment.Status.PENDING).select_related(
            "post",
            "author",
            "post__author",
        )
        if not user_is_admin(self.request.user):
            queryset = queryset.filter(post__author=self.request.user)
        return queryset


class CommentModerationActionView(AnimateurRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment.objects.select_related("post", "post__author"), pk=kwargs["pk"])
        if not can_moderate_comment(request.user, comment):
            raise PermissionDenied("Vous ne pouvez modérer que les commentaires de vos propres articles.")
        action = kwargs["action"]
        if action == "approve":
            comment.status = Comment.Status.APPROVED
            message = "Commentaire validé."
        else:
            comment.status = Comment.Status.REJECTED
            message = "Commentaire rejeté."
        comment.save(update_fields=["status"])
        messages.success(request, message)
        return redirect("moderation-comments")


class AdvertisementCreateView(CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "ads/ad_form.html"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.submitted_by = self.request.user
        form.instance.status = Advertisement.Status.PENDING
        messages.info(
            self.request,
            "Publicité soumise. Elle sera visible après validation par un modérateur.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return "/ads/"


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = "ads/ad_list.html"
    context_object_name = "ads"

    def get_queryset(self):
        return Advertisement.objects.filter(status=Advertisement.Status.APPROVED)


class AdvertisementModerationListView(AnimateurRequiredMixin, ListView):
    model = Advertisement
    template_name = "ads/moderation_ads.html"
    context_object_name = "ads"

    def get_queryset(self):
        return Advertisement.objects.filter(status=Advertisement.Status.PENDING)


class AdvertisementModerationActionView(AnimateurRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ad = get_object_or_404(Advertisement, pk=kwargs["pk"])
        action = kwargs["action"]
        if action == "approve":
            ad.status = Advertisement.Status.APPROVED
            ad.validated_at = timezone.now()
            message = "Publicité validée."
        else:
            ad.status = Advertisement.Status.REJECTED
            message = "Publicité rejetée."
        ad.save(update_fields=["status", "validated_at"])
        messages.success(request, message)
        return redirect("moderation-ads")
