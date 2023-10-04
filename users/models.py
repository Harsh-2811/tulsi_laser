from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    class Roles(models.TextChoices):
        admin = "admin", "Admin"
        technician = "technician", "Technician"
        customer = "customer", "Customer"
        site_user = "site_user", "Site User"

    email = models.CharField(null=True, blank=True, max_length=265)
    role = models.CharField(choices=Roles.choices, max_length=50)
    
