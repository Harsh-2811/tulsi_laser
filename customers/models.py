from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class MachineType(models.Model):
    class Statuses(models.IntegerChoices):
        in_active = 0, "In Active"
        active = 1, "Active"
    _type = models.CharField(max_length=200, verbose_name="Machine Type")
    status = models.IntegerField(choices=Statuses.choices, default=Statuses.active)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_

class Customer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    company_name = models.CharField(max_length=265)
    company_mobile_no = PhoneNumberField()
    manager_name = models.CharField(max_length=265)
    manager_mobile_no = models.CharField(max_length=265)
    address = models.TextField(null=True, blank=True)
    complain_limit = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class Machine(models.Model):
    class Warranty(models.TextChoices):
        yearly = "yearly", "Yearly"
        monthly = "monthly", "Monthly"

    code = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    machine_type = models.ForeignKey(MachineType, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    warranty = models.CharField(choices=Warranty.choices, max_length=100)
    duration = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.company_name} => {self.machine_type._type}"

    
class Technician(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    phone_1 = PhoneNumberField()
    phone_2 = PhoneNumberField(null=True, blank=True)
    expertise = models.CharField(max_length=265, null=True, blank=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}, {self.phone_1}"
    