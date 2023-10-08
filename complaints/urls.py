from django.urls import path
from .views import Complaints, getCompanyByMachine, getMachinesByCustomer
urlpatterns = [
    path("complaints/",Complaints.as_view(), name="complaints"),
    path("getCompanyByMachine/", getCompanyByMachine, name="getCompanyByMachine"),
    path("getMachinesByCustomer/", getMachinesByCustomer, name="getMachinesByCustomer"),

]