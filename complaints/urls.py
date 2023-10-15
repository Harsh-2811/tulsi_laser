from django.urls import path
from .views import Complaints, getCompanyByMachine, getMachinesByCustomer, getAddressByCustomer, checkIfComplainExistForDay, EditComplain, DeleteComplain, Payments, EditPayment, DeletePayment, Services, EditService, DeleteService
urlpatterns = [
    path("complaints/",Complaints.as_view(), name="complaints"),
    path("getCompanyByMachine/", getCompanyByMachine, name="getCompanyByMachine"),
    path("getMachinesByCustomer/", getMachinesByCustomer, name="getMachinesByCustomer"),
    path("getAddressByCustomer/", getAddressByCustomer, name="getAddressByCustomer"),
    path("checkIfComplainExistForDay/<int:mid>/", checkIfComplainExistForDay, name="checkIfComplainExistForDay"),

    path("complaints/edit/<int:pk>/",EditComplain.as_view(),name="edit_complaints"),
    path("complaints/delete/<int:pk>/",DeleteComplain.as_view(),name="delete_complaints"),

    path("payments/",Payments.as_view(), name="payments"),
    path("payments/edit/<int:pk>/",EditPayment.as_view(),name="edit_payments"),
    path("payments/delete/<int:pk>/",DeletePayment.as_view(),name="delete_payments"),

    path("services/",Services.as_view(), name="services"),
    path("services/edit/<int:pk>/",EditService.as_view(),name="edit_services"),
    path("services/delete/<int:pk>/",DeleteService.as_view(),name="delete_services"),

]