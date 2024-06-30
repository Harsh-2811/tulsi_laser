from django.db import models
from customers.models import Machine, Customer
from users.models import Technician
from django.utils import timezone

# Create your models here.

class Complain(models.Model):
    class Statuses(models.IntegerChoices):
        all = 0, "All"
        new = 1, "New"
        pending = 2, "Pending"
        running = 3, "Running"
        completed = 4, "Completed"
    
    class TechStatuses(models.IntegerChoices):
        pending = 2, "Pending"
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
    
    @property
    def repeated_today(self):
        is_complain_exits = Complain.objects.filter(machine = self.machine, date = self.date).count()
        return is_complain_exits
    
    @property
    def solution(self):
        if self.status == self.Statuses.completed:
            if ComplainOutcome.objects.filter(complain = self).first():
                return ComplainOutcome.objects.filter(complain = self).first().remark
        return None
    
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

    completed_date = models.DateField(null=True, blank=True)
    completed_by = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, blank=True, related_name="service_solutions")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_details
    

class ComplainOutcome(models.Model):
    class Complaint_types(models.TextChoices):
        genuine = "Genuine", "Genuine"
        fake = "Fake", "Fake"
        
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE,null=True, blank=True)
    complaint_type = models.CharField(choices=Complaint_types.choices, max_length=50)
    challan = models.CharField(null=True, blank=True, max_length=20) 
    remark = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    signature = models.ImageField(upload_to="signature",null=True, blank=True)
    alignment = models.BooleanField(default=False,null=True, blank=True)
    ampere = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True) 
    watt = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True) 
    temp = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    voltage = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    water_filter = models.BooleanField(default=False,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean_string(self, string):
        import re
        # Replace newline characters with a space
        string = string.replace('\n', ' ')
        # Use regular expression to replace non-alphanumeric characters (excluding spaces) with an empty string
        cleaned_string = re.sub(r'[^A-Za-z0-9\s]', '', string)
        return cleaned_string

    def save(self, *args, **kwargs):
        self.remark = self.clean_string(self.remark)
        super(ComplainOutcome, self).save(*args, **kwargs)
