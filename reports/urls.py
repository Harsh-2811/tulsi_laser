from django.urls import path
from .views import ComplaintReport, MachineTypeReport, PaymentReport
urlpatterns = [
    path("complaints/",ComplaintReport.as_view(), name="report_complaints"),
    path("machine_types/",MachineTypeReport.as_view(), name="report_machine_types"),
    path("payment/",PaymentReport.as_view(), name="report_payment"),

]