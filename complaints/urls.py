from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import Complaints, getCompanyByMachine, getMachinesByCustomer, getAddressByCustomer, checkIfComplainExistForDay, EditComplain, DeleteComplain, Payments, EditPayment, DeletePayment, Services, EditService, DeleteService, getComplaintOutcomeByMachine, checkIfLimitOver, updateStatusToRunning, getComplaintOutcomeByMachineId, ComplainOutcomeCreate
urlpatterns = [
    path("complaints/",login_required(Complaints.as_view()), name="complaints"),


    path("getComplaintOutcomeByMachine/",login_required(getComplaintOutcomeByMachine), name="getComplaintOutcomeByMachine"),
    path("getComplaintOutcomeByMachine/<int:machine_id>/",login_required(getComplaintOutcomeByMachineId), name="getComplaintOutcomeByMachine"),

    path("checkIfLimitOver/",login_required(checkIfLimitOver), name="checkIfLimitOver"),


    path("getCompanyByMachine/", login_required(getCompanyByMachine), name="getCompanyByMachine"),
    path("getMachinesByCustomer/", login_required(getMachinesByCustomer), name="getMachinesByCustomer"),
    path("getAddressByCustomer/", login_required(getAddressByCustomer), name="getAddressByCustomer"),
    path("checkIfComplainExistForDay/<int:mid>/", login_required(checkIfComplainExistForDay), name="checkIfComplainExistForDay"),

    path("complaints/edit/<int:pk>/",login_required(EditComplain.as_view()),name="edit_complaints"),
    path("complaints/delete/<int:pk>/",login_required(DeleteComplain.as_view()),name="delete_complaints"),

    path("payments/",login_required(Payments.as_view()), name="payments"),
    path("payments/edit/<int:pk>/",login_required(EditPayment.as_view()),name="edit_payments"),
    path("payments/delete/<int:pk>/",login_required(DeletePayment.as_view()),name="delete_payments"),

    path("services/",login_required(Services.as_view()), name="services"),
    path("services/edit/<int:pk>/",login_required(EditService.as_view()),name="edit_services"),
    path("services/delete/<int:pk>/",login_required(DeleteService.as_view()),name="delete_services"),
    path("updateStatusToRunning/<int:id>/", login_required(updateStatusToRunning), name="updateStatusToRunning"),
    path("completeComplain/", login_required(ComplainOutcomeCreate.as_view()), name="completeComplain")
]