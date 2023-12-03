from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from customers.models import Customer, Machine, MachineType
import os
import pandas as pd
from users.models import User

class Command(BaseCommand):
    help = 'Import Excel File'

    def add_arguments(self, parser):
        parser.add_argument('sheet_name', type=str)
        parser.add_argument('-s', '--skip_row', type=str )

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "machine_details.xlsx")
        sheet_name = kwargs['sheet_name']
        skip_row = kwargs['skip_row']
        print(sheet_name)
        xls = pd.ExcelFile(file_path)
        df1 = pd.read_excel(xls, sheet_name,skiprows=int(skip_row))
    
        print(f"Columns in Excel: {df1.columns}")

        for index, row in df1.iterrows():
            # Use correct column names
            try:
                machine_type = MachineType.objects.get(_type=row['MACHINE TYPE'] if row.get('MACHINE TYPE') else row['MACHINE NAME'])
            except MachineType.DoesNotExist:
                machine_type = MachineType.objects.create(_type=row['MACHINE TYPE'] if row.get('MACHINE TYPE') else row['MACHINE NAME'])

            try:
                customer = Customer.objects.get(company_name=row['PARTY NAME'], )
            except Customer.DoesNotExist:
                email = "tulsilasertec@gmail.com"
                try:
                    user = User.objects.get(username=row['PARTY NAME'])
                except User.DoesNotExist:
                    user = User.objects.create_user(username=row['PARTY NAME'], email=email, first_name=row['PARTY NAME'], password="TulsiLaser@123", role=User.Roles.customer)

                customer = Customer.objects.create(company_name=row['PARTY NAME'], address=row.get('ADD.'), user=user)

            try:
                machine = Machine.objects.get(code=row['TYPE NO'] if row.get('TYPE NO') else row['MACHINE NO'])
            except Machine.DoesNotExist:
                machine = Machine.objects.create(code=row['TYPE NO'] if row.get('TYPE NO') else row['MACHINE NO'], machine_type=machine_type, purchase_date=row['DATE'], customer=customer, duration=10, warranty = Machine.Warranty.yearly)