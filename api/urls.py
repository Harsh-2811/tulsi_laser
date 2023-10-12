from django.urls import path
from customers.views import  AddCustomer
# from .views import UserLogIn
from customers.views import MachineTypes, AddCustomer, EdiMachineType, DeleteMachineType, Customers, EdiCustomers, DeleteCustomers
from rest_framework.authtoken import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    
    path("login/", obtain_auth_token, name="obtain-auth-token"),


]