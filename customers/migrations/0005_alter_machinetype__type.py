# Generated by Django 4.2.5 on 2023-10-06 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_alter_customer_company_mobile_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinetype',
            name='_type',
            field=models.CharField(max_length=200, unique=True, verbose_name='Machine Type'),
        ),
    ]