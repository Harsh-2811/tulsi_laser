# Generated by Django 4.2.5 on 2023-10-09 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_technician_phone_1_alter_technician_phone_2'),
        ('customers', '0006_alter_machine_customer'),
        ('complaints', '0005_payment_end_date_payment_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='technician',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.technician'),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('service_details', models.CharField(max_length=265)),
                ('in_serial_no', models.CharField(max_length=265)),
                ('out_serial_no', models.CharField(max_length=265)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.machine')),
                ('technician', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.technician')),
            ],
        ),
    ]
