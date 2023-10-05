from django.db import models
from customers.models import Machine, Customer
from users.models import Technician
# Create your models here.

class Complain(models.Model):
    class Statuses(models.IntegerChoices):
        all = 0, "All"
        new = 1, "New"
        pending = 2, "Pending"
        running = 3, "Running"
        completed = 4, "Completed"

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    issue = models.CharField(max_length=255)
    date = models.DateField()
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Statuses.choices, default=Statuses.new)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
