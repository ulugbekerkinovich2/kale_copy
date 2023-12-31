# Generated by Django 4.2.3 on 2023-08-12 11:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0002_comparison"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkout",
            name="comment",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="checkout",
            name="district",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="checkout",
            name="installation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="checkout",
            name="isNewAddress",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="checkout",
            name="paymentType",
            field=models.IntegerField(choices=[(0, "CASH"), (1, "PAYME"), (2, "CLICK"), (3, "UZUM")], default=0),
        ),
        migrations.AddField(
            model_name="checkout",
            name="region",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="checkout",
            name="street",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
