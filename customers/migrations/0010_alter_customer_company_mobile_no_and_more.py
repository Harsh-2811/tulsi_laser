# Generated by Django 4.2.5 on 2023-12-03 06:41

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0009_machine_warranty_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="company_mobile_no",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, null=True, region=None
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="manager_mobile_no",
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="manager_name",
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
    ]
