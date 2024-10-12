# Generated by Django 5.1.1 on 2024-10-09 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vnineapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Employee",
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
                ("name", models.CharField(max_length=100)),
                (
                    "role",
                    models.CharField(
                        choices=[("Driver", "Driver"), ("Loadman", "Loadman")],
                        max_length=20,
                    ),
                ),
                ("phone_number", models.CharField(max_length=15, unique=True)),
                ("date_of_joining", models.DateField()),
            ],
        ),
    ]
