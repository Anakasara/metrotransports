# Generated by Django 5.1.1 on 2024-10-09 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vnineapp", "0004_attendance"),
    ]

    operations = [
        migrations.CreateModel(
            name="TractorHours",
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
                ("date", models.DateField()),
                ("start_hour", models.FloatField()),
                ("end_hour", models.FloatField()),
                ("total_hours", models.FloatField()),
                (
                    "tractor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hours",
                        to="vnineapp.tractor",
                    ),
                ),
            ],
            options={
                "unique_together": {("tractor", "date")},
            },
        ),
    ]
