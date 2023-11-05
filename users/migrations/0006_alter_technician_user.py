# Generated by Django 4.2.5 on 2023-11-04 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_technician_app_access_technician_web_access"),
    ]

    operations = [
        migrations.AlterField(
            model_name="technician",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
