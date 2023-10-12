from django.db import models
from customers.models import Machine, Customer
from users.models import Technician
# Create your models here.

class Complain(models.Model):
    class Statuses(models.IntegerChoices):
        all = 0, "All"
        new = 1, "New"
        accepted = 2, "Accepted"
        running = 3, "Running"
        completed = 4, "Completed"
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    issue = models.CharField(max_length=255)
    date = models.DateField()
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=Statuses.choices, default=Statuses.new)
    address = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.customer.company_name}, {self.machine.code}, {self.date}"
    
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Service(models.Model):

    class Statuses(models.IntegerChoices):
        active = 1, "Active"
        completed = 2, "Completed"

    date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True)
    service_details = models.CharField(max_length=265)
    in_serial_no = models.CharField(max_length=265)
    out_serial_no = models.CharField(max_length=265)
    status = models.IntegerField(choices=Statuses.choices, default=Statuses.active)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ComplainOutcome(models.Model):
    class Complaint_types(models.TextChoices):
        genuine = "Genuine", "Genuine"
        fake = "Fake", "Fake"
        
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    complaint_type = models.CharField(choices=Complaint_types.choices, max_length=50)
    challan = models.IntegerField(null=True, blank=True) 
    remark = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    signature = models.CharField(max_length=255)
    alignment = models.BooleanField(default=False,null=True, blank=True)
    ampere = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True) 
    temp = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    voltage = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    water_filter = models.BooleanField(default=False,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)