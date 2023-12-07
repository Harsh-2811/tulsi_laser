# Generated by Django 4.2.5 on 2023-12-07 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_apks_options_alter_technician_address"),
        ("complaints", "0016_alter_complainoutcome_signature"),
    ]

    operations = [
        migrations.AlterField(
            model_name="complainoutcome",
            name="technician",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.technician",
            ),
        ),
    ]
