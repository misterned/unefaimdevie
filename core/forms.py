from django import forms

from .models import Advertisement, Comment, Post


class QuillWidget(forms.Textarea):
    """Textarea remplacé par l'éditeur Quill au rendu."""

    def __init__(self, toolbar='simple', *args, **kwargs):
        self.toolbar = toolbar
        super().__init__(*args, **kwargs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-quill'] = self.toolbar
        return attrs

    class Media:
        css = {'all': ('https://cdn.quilljs.com/1.3.7/quill.snow.css',)}
        js = (
            'https://cdn.quilljs.com/1.3.7/quill.min.js',
            'core/js/quill-init.js',
        )


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
        widgets = {
            "body": QuillWidget(toolbar='rich'),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) > 150:
            raise forms.ValidationError("Le titre ne doit pas dépasser 150 caractères.")
        return title


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ["title", "merchant", "image", "text", "price"]
        widgets = {
            "text": QuillWidget(toolbar='simple'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].max_length = None


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author_name", "author_email", "content"]
        widgets = {
            "author_name": forms.TextInput(attrs={"placeholder": "Votre nom"}),
            "author_email": forms.EmailInput(attrs={"placeholder": "Votre email (optionnel)"}),
            "content": forms.Textarea(attrs={"rows": 4, "placeholder": "Votre commentaire"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author_email"].required = False



