# Generated by Django 4.2.5 on 2023-10-11 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("complaints", "0008_rename_end_date_payment_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="status",
            field=models.IntegerField(
                choices=[(1, "Active"), (2, "Completed")], default=1, max_length=100
            ),
        ),
    ]
