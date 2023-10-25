from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    class Roles(models.TextChoices):
        admin = "admin", "Admin"
        technician = "technician", "Technician"
        customer = "customer", "Customer"
        site_user = "site_user", "Site User"

    email = models.CharField(null=True, blank=True, max_length=265)
    role = models.CharField(choices=Roles.choices, max_length=50)
    
class Technician(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_1 = PhoneNumberField(unique=True)
    phone_2 = PhoneNumberField(null=True, blank=True, unique=True)
    expertise = models.CharField(max_length=265, null=True, blank=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.phone_1})"
    