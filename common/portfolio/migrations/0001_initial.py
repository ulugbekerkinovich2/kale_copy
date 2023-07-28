# Generated by Django 4.2.3 on 2023-07-20 19:35

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Portfolio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("title", models.CharField(max_length=250)),
                ("description", ckeditor.fields.RichTextField()),
                ("photo", models.ImageField(upload_to="portfolioImage", verbose_name="Image of Portfolio")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PortfolioImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="portfolioImage", verbose_name="Image of Product"
                    ),
                ),
                (
                    "portfolio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="portfolioImages",
                        to="portfolio.portfolio",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
