from django.contrib import admin
from .models import MachineType ,Machine,Customer 
# Register your models here.

admin.site.register(MachineType)

admin.site.register(Machine)
admin.site.register(Customer)