from django.urls import path
from customers.views import AddMachineType, AddCustomer
from django.urls import path
from .views import ComplainCreateView, ComplainUpdateView, ComplainRetrieveView

urlpatterns = [
    path("add_machine_type/",AddMachineType.as_view(), name="add_machine_type"),
    path("add_customer/",AddCustomer.as_view(), name="add_customer"),
    path('complains/', ComplainCreateView.as_view(), name='complain-create'),
    path('complains/<int:pk>/', ComplainUpdateView.as_view(), name='complain-update'),
    path('complains/<int:pk>/', ComplainRetrieveView.as_view(), name='complain-retrieve'),
]