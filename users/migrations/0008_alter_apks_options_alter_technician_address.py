# Generated by Django 4.2.5 on 2023-11-11 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_apks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apks',
            options={'verbose_name': 'APKs'},
        ),
        migrations.AlterField(
            model_name='technician',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]