# Generated by Django 4.2.3 on 2023-08-09 17:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_catalog_description_en_catalog_description_ru_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="catalogimage",
            old_name="portfolio",
            new_name="catalog",
        ),
    ]
