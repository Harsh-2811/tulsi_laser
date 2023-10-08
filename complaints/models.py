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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    issue = models.CharField(max_length=255)
    date = models.DateField()
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Statuses.choices, default=Statuses.new)
    address = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.customer.company_name}, {self.machine.code}, {self.date}"
    