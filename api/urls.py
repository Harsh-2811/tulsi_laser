from django.urls import path
from customers.views import  AddCustomer
from .views import UserLogIn
from customers.views import MachineTypes, AddCustomer, EdiMachineType, DeleteMachineType, Customers, EdiCustomers, DeleteCustomers
from rest_framework.authtoken import views

urlpatterns = [
    path('api-user-login/', UserLogIn.as_view()),
]