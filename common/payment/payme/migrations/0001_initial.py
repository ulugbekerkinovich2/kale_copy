# Generated by Django 4.2.3 on 2023-07-24 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("amount", models.FloatField(default=0, null=True)),
                ("paymentType", models.IntegerField(choices=[(1, "PAYME"), (2, "CLICK"), (3, "UZUM")])),
                ("discount", models.IntegerField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("waiting", "WAITING"),
                            ("preauth", "PREAUTH"),
                            ("confirmed", "CONFIRMED"),
                            ("rejected", "REJECTED"),
                            ("refunded", "REFUNDED"),
                            ("error", "ERROR"),
                        ],
                        default="waiting",
                        max_length=20,
                    ),
                ),
                ("orders", models.ManyToManyField(blank=True, related_name="orderPayment", to="order.order")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="userPayment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PaymentVerification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("token", models.CharField(max_length=500)),
                ("time", models.DateTimeField(auto_now_add=True)),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="paymentVerify", to="payme.payment"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
