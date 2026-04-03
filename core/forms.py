from django import forms

from .models import Advertisement, Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "body",
            "image",
            "category",
            "status",
            "notebook_html",
            "powerbi_embed_code",
            "video_url",
            "video_file",
        ]

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) > 150:
            raise forms.ValidationError("Le titre ne doit pas dépasser 150 caractères.")
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "placeholder": "Votre commentaire"}),
        }


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ["title", "merchant", "image", "text", "price"]
