# Generated by Django 4.2.3 on 2023-07-21 10:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="file",
        ),
        migrations.RemoveField(
            model_name="message",
            name="photo",
        ),
        migrations.RemoveField(
            model_name="message",
            name="type",
        ),
        migrations.AlterField(
            model_name="message",
            name="content",
            field=models.TextField(default="test"),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="Contact",
        ),
    ]
