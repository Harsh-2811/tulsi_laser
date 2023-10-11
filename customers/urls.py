from django.urls import path
from customers.views import  AddCustomer
from .views import ComplainCreateView, ComplainUpdateView, ComplainRetrieveView

from customers.views import MachineTypes, AddCustomer, EdiMachineType, DeleteMachineType, Customers, EdiCustomers, DeleteCustomers
urlpatterns = [
    path("machine_types/",MachineTypes.as_view(), name="machine_types"),
    path("machine_type/edit/<int:pk>/",EdiMachineType.as_view(),name="edit_machine_type"),
    path("machine_type/delete/<int:pk>/",DeleteMachineType.as_view(),name="delete_machine_type"),
    path("add_customer/",AddCustomer.as_view(), name="add_customer"),
    path('complains/', ComplainCreateView.as_view(), name='complain-create'),
    path('complains/<int:pk>/', ComplainUpdateView.as_view(), name='complain-update'),
    path('complains/<int:pk>/', ComplainRetrieveView.as_view(), name='complain-retrieve'),

    path("customers/",Customers.as_view(), name="customers"),
    path("customers/edit/<int:pk>/",EdiCustomers.as_view(),name="edit_customers"),
    path("customers/delete/<int:pk>/",DeleteCustomers.as_view(),name="delete_customers"),

]