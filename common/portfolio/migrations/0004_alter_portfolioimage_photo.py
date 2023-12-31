# Generated by Django 4.2.3 on 2023-08-16 21:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0003_portfolio_description_en_portfolio_description_ru_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="portfolioimage",
            name="photo",
            field=models.ImageField(
                blank=True, null=True, upload_to="portfolioImage", verbose_name="Image of Portfolio"
            ),
        ),
    ]
