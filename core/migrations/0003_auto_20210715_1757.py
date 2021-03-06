# Generated by Django 3.1.5 on 2021-07-15 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_about_document"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contacts",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="page title")),
                ("content", models.TextField(verbose_name="page content")),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="email to copy"),
                ),
                (
                    "published",
                    models.BooleanField(default=False, verbose_name="published"),
                ),
            ],
            options={
                "verbose_name": "Contacts page",
                "verbose_name_plural": "Contacts page",
            },
        ),
        migrations.AlterModelOptions(
            name="about",
            options={"verbose_name": "About page", "verbose_name_plural": "About page"},
        ),
        migrations.CreateModel(
            name="Link",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="link name")),
                ("url", models.URLField(verbose_name="URL")),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.contacts"
                    ),
                ),
            ],
        ),
    ]
