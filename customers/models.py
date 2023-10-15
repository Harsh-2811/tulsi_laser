from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, timedelta
# Create your models here.
class MachineType(models.Model):
    class Statuses(models.IntegerChoices):
        in_active = 0, "In Active"
        active = 1, "Active"
    _type = models.CharField(max_length=200, verbose_name="Machine Type", unique=True)
    status = models.IntegerField(choices=Statuses.choices, default=Statuses.active)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self._type

    def html_status(self):
        from django.utils.html import format_html
        if self.status:
            return format_html('<span class="badge badge-soft-success">Active</span>') 
        else:
            return format_html('<span class="badge badge-soft-warning">In Active</span>') 


class Customer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    company_name = models.CharField(max_length=265)
    company_mobile_no = PhoneNumberField(unique=True)
    manager_name = models.CharField(max_length=265)
    manager_mobile_no = models.CharField(max_length=265, unique=True)
    complain_limit = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class Machine(models.Model):
    class Warranty(models.TextChoices):
        yearly = "yearly", "Yearly"
        monthly = "monthly", "Monthly"

    code = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="machines")
    machine_type = models.ForeignKey(MachineType, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    warranty = models.CharField(choices=Warranty.choices, max_length=100)
    duration = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code}"
    
    @property
    def total_complaints(self):
        from complaints.models import Complain
        return Complain.objects.filter(machine = self).count()
    
    @property
    def warranty_ends_this_month(self):
        warranty = self.warranty
        duration = self.duration
        if warranty == Machine.Warranty.yearly:
            days = ((duration*365)+duration//4)
            print(days)
            warranty_ends_in = self.created_at + timedelta(days=int(days))
        elif warranty == Machine.Warranty.monthly:
            days = duration * 30
            warranty_ends_in = self.created_at + timedelta(days=days)
        
        today_month = datetime.today().month
        end_month = warranty_ends_in.month

        current_year = datetime.today().year
        end_year = warranty_ends_in.year

        if today_month == end_month and current_year == end_year:
            return "Yes"

        return f"No (Ending Date : {warranty_ends_in.strftime('%d-%m-%Y')})"