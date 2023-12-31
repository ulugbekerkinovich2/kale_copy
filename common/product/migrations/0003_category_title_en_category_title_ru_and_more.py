# Generated by Django 4.2.3 on 2023-08-06 12:57

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_alter_category_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="title_en",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="title_ru",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="title_uz",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="brand_en",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="brand_ru",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="brand_uz",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="description_en",
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="description_ru",
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="description_uz",
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="manufacturer_en",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="manufacturer_ru",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="manufacturer_uz",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="material_en",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="material_ru",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="material_uz",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="title_en",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="title_ru",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="title_uz",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="subcategory",
            name="title_en",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="subcategory",
            name="title_ru",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="subcategory",
            name="title_uz",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
