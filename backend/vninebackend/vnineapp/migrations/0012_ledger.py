# Generated by Django 5.1.1 on 2024-10-09 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vnineapp", "0011_delete_sale"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ledger",
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
                ("description", models.CharField(max_length=255)),
                ("amount_dr", models.DecimalField(decimal_places=2, max_digits=10)),
                ("amount_cr", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vnineapp.customer",
                    ),
                ),
            ],
        ),
    ]
