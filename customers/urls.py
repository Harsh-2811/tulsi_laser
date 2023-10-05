from django.urls import path
from customers.views import AddMachineType, AddCustomer
urlpatterns = [
    path("add_machine_type/",AddMachineType.as_view(), name="add_machine_type"),
    path("add_customer/",AddCustomer.as_view(), name="add_customer"),

]