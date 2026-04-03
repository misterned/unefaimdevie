from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AdvertisementForm, CommentForm, PostForm
from .models import Advertisement, Comment, Post


class AnimateurRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_superuser or user.is_staff or user.groups.filter(name="animateur").exists()
        )


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

    def form_valid(self, form):
        messages.success(self.request, "Article modifié avec succès.")
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        form.instance.status = Comment.Status.PENDING
        messages.info(
            self.request,
            "Commentaire soumis. Il sera publié après validation par un animateur.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.post.get_absolute_url()


class CommentModerationListView(AnimateurRequiredMixin, ListView):
    model = Comment
    template_name = "posts/moderation_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(status=Comment.Status.PENDING).select_related("post", "author")


class CommentModerationActionView(AnimateurRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs["pk"])
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


class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "ads/ad_form.html"

    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        form.instance.status = Advertisement.Status.PENDING
        messages.info(
            self.request,
            "Publicité soumise. Elle sera visible après validation par un animateur.",
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
