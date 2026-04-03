import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="notebook_html",
            field=models.FileField(
                blank=True,
                help_text="HTML pré-généré depuis un notebook (nbconvert).",
                null=True,
                upload_to="posts/notebooks/",
                validators=[django.core.validators.FileExtensionValidator(["html", "htm"])],
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="video_file",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="posts/videos/",
                validators=[django.core.validators.FileExtensionValidator(["mp4", "webm", "ogg"])],
            ),
        ),
    ]
