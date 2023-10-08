# Generated by Django 4.2.5 on 2023-10-08 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_alter_machinetype__type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machines', to='customers.customer'),
        ),
    ]
