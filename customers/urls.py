from django.urls import path
from customers.views import  AddCustomer
from .views import ComplainCreateView, ComplainUpdateView, ComplainRetrieveView
from django.contrib.auth.decorators import login_required

from customers.views import MachineTypes, AddCustomer, EdiMachineType, DeleteMachineType, Customers, EdiCustomers, DeleteCustomers
urlpatterns = [
    path("machine_types/",login_required(MachineTypes.as_view()), name="machine_types"),
    path("machine_type/edit/<int:pk>/",login_required(EdiMachineType.as_view()),name="edit_machine_type"),
    path("machine_type/delete/<int:pk>/",login_required(DeleteMachineType.as_view()),name="delete_machine_type"),
    path("add_customer/",login_required(AddCustomer.as_view()), name="add_customer"),
    path('complains/', login_required(ComplainCreateView.as_view()), name='complain-create'),
    path('complains/<int:pk>/', login_required(ComplainUpdateView.as_view()), name='complain-update'),
    path('complains/<int:pk>/', login_required(ComplainRetrieveView.as_view()), name='complain-retrieve'),

    path("customers/",login_required(Customers.as_view()), name="customers"),
    path("customers/edit/<int:pk>/",login_required(EdiCustomers.as_view()),name="edit_customers"),
    path("customers/delete/<int:pk>/",login_required(DeleteCustomers.as_view()),name="delete_customers"),

]