from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from customers.models import Customer, Machine, MachineType
import os
import pandas as pd
import numpy as np
from users.models import User

class Command(BaseCommand):
    help = 'Import Excel File'

    def add_arguments(self, parser):
        parser.add_argument('sheet_name', type=str)
        parser.add_argument('-s', '--skip_row', type=str )

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "all_machine_list.xlsx")
        sheet_name = kwargs['sheet_name']
        skip_row = kwargs['skip_row']
        print(sheet_name)
        xls = pd.ExcelFile(file_path)
        df1 = pd.read_excel(xls, sheet_name,skiprows=int(skip_row))
        df1.fillna(0, inplace=True)
      
        print(f"Columns in Excel: {df1.columns}")
        MachineType.objects.all().delete()
        Machine.objects.all().delete()
        Customer.objects.all().delete()
        for index, row in df1.iterrows():
            # Use correct column names
            __type = row['MACHINE TYPE'] if row.get('MACHINE TYPE') else row['MACHINE NAME']
            if not __type or __type == "nan":
                continue
            _type = str(__type).strip()
            try:
                machine_type = MachineType.objects.get(_type=_type)
            except MachineType.DoesNotExist:
                machine_type = MachineType.objects.create(_type=_type)

            try:
                customer = Customer.objects.get(company_name=row['PARTY NAME'] )
            except Customer.DoesNotExist:
                email = "tulsilasertec@gmail.com"
                try:
                    user = User.objects.get(username=row['PARTY NAME'])
                except User.DoesNotExist:
                    user = User.objects.create_user(username=row['PARTY NAME'], email=email, first_name=row['PARTY NAME'], password="TulsiLaser@123", role=User.Roles.customer)

                if not row['CONTACT NO']:
                
                    customer = Customer.objects.create(company_name=row['PARTY NAME'], address=row.get('ADDRESS'), user=user)
                else:
                    customer = Customer.objects.create(company_name=row['PARTY NAME'], address=row.get('ADDRESS'), user=user, company_mobile_no=f"+91 {row['CONTACT NO']}" if row['CONTACT NO'] not in ("nan", None) else "")

            if row.get('TYPE NO'):
                try:
                    machine = Machine.objects.get(code=row['TYPE NO'])
                except Machine.DoesNotExist:
                    machine = Machine.objects.create(code=row['TYPE NO'], machine_type=machine_type, purchase_date=row['DATE'], customer=customer, duration=10, warranty = Machine.Warranty.yearly)
            else:
                machine = Machine.objects.create(code=row['TYPE NO'], machine_type=machine_type, purchase_date=row['DATE'], customer=customer, duration=10, warranty = Machine.Warranty.yearly)
