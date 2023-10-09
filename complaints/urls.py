from django.urls import path
from .views import Complaints, getCompanyByMachine, getMachinesByCustomer, EditComplain, DeleteComplain, Payments, EditPayment, DeletePayment
urlpatterns = [
    path("complaints/",Complaints.as_view(), name="complaints"),
    path("getCompanyByMachine/", getCompanyByMachine, name="getCompanyByMachine"),
    path("getMachinesByCustomer/", getMachinesByCustomer, name="getMachinesByCustomer"),
    path("complaints/edit/<int:pk>/",EditComplain.as_view(),name="edit_complaints"),
    path("complaints/delete/<int:pk>/",DeleteComplain.as_view(),name="delete_complaints"),

    path("payments/",Payments.as_view(), name="payments"),
    path("payments/edit/<int:pk>/",EditPayment.as_view(),name="edit_payments"),
    path("payments/delete/<int:pk>/",DeletePayment.as_view(),name="delete_payments"),
]