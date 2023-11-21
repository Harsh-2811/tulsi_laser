# Generated by Django 4.2.5 on 2023-10-29 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_technician_phone_1_alter_technician_phone_2"),
        ("complaints", "0013_complainoutcome_watt"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="solution_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="solution_technician",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="service_solutions",
                to="users.technician",
            ),
        ),
        migrations.AlterField(
            model_name="complainoutcome",
            name="signature",
            field=models.ImageField(upload_to="signature"),
        ),
    ]
