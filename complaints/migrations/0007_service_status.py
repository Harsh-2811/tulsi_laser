# Generated by Django 4.2.5 on 2023-10-09 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("complaints", "0006_alter_complain_technician_service"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="status",
            field=models.CharField(
                choices=[("active", "Active"), ("completed", "Completed")],
                default="active",
                max_length=100,
            ),
        ),
    ]
