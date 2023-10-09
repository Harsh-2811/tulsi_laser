# Generated by Django 4.2.5 on 2023-10-08 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("complaints", "0002_alter_complain_technician"),
    ]

    operations = [
        migrations.AlterField(
            model_name="complain",
            name="status",
            field=models.IntegerField(
                choices=[
                    (0, "All"),
                    (1, "New"),
                    (2, "Accepted"),
                    (3, "Running"),
                    (4, "Completed"),
                ],
                default=1,
            ),
        ),
    ]
