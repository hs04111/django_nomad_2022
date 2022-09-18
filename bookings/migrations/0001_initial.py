# Generated by Django 4.1.1 on 2022-09-16 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("experiences", "0002_experience_category_alter_perk_details"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rooms", "0002_room_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "kind",
                    models.CharField(
                        choices=[("room", "Room"), ("experience", "Experience")],
                        max_length=15,
                    ),
                ),
                ("check_in", models.DateField(blank=True, null=True)),
                ("check_out", models.DateField(blank=True, null=True)),
                ("experience_time", models.DateTimeField(blank=True, null=True)),
                ("guests", models.PositiveIntegerField()),
                (
                    "experience",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="experiences.experience",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="rooms.room",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
