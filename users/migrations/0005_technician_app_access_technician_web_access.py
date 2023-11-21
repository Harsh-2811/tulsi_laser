# Generated by Django 4.2.5 on 2023-11-04 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_user_push_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="technician",
            name="app_access",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="technician",
            name="web_access",
            field=models.BooleanField(default=False),
        ),
    ]
