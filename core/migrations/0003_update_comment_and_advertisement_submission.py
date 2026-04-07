from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def get_user_identifier(user):
    username_field = getattr(user, "USERNAME_FIELD", "username")
    username = getattr(user, username_field, "")
    if username:
        return username

    fallback_username = getattr(user, "username", "")
    if fallback_username:
        return fallback_username

    return str(user)


def populate_comment_author_name(apps, schema_editor):
    Comment = apps.get_model("core", "Comment")

    for comment in Comment.objects.select_related("author").all():
        if comment.author_id and not comment.author_name:
            comment.author_name = get_user_identifier(comment.author)
            comment.author_email = comment.author.email or ""
            comment.save(update_fields=["author_name", "author_email"])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0002_alter_post_notebook_html_alter_post_video_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advertisement",
            name="submitted_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="advertisements",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="author_email",
            field=models.EmailField(blank=True, max_length=254, verbose_name="Email"),
        ),
        migrations.AddField(
            model_name="comment",
            name="author_name",
            field=models.CharField(default="", max_length=120, verbose_name="Nom"),
        ),
        migrations.RunPython(populate_comment_author_name, migrations.RunPython.noop),
    ]