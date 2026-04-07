from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_update_comment_and_advertisement_submission"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="advertisement",
            name="submitted_by",
        ),
        migrations.RemoveField(
            model_name="advertisement",
            name="validated_at",
        ),
        migrations.AddField(
            model_name="advertisement",
            name="featured",
            field=models.BooleanField(default=False, verbose_name="À la une"),
        ),
        migrations.AlterField(
            model_name="advertisement",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Brouillon"),
                    ("approved", "Visible"),
                    ("rejected", "Archivée"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
    ]
