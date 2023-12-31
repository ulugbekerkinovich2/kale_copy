# Generated by Django 4.2.3 on 2023-08-07 10:17

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("partner", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="partner",
            name="description_en",
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name="partner",
            name="description_ru",
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name="partner",
            name="description_uz",
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name="partner",
            name="title_en",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="partner",
            name="title_ru",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="partner",
            name="title_uz",
            field=models.CharField(max_length=250, null=True),
        ),
    ]
