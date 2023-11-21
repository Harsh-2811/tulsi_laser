from django.urls import path
from .views import ComplaintReport, MachineTypeReport, PaymentReport, ServiceReport, TechnicianReport
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("complaints/",login_required(ComplaintReport.as_view()), name="report_complaints"),
    path("machine_types/",login_required(MachineTypeReport.as_view()), name="report_machine_types"),
    path("payment/",login_required(PaymentReport.as_view()), name="report_payment"),
    path("service/",login_required(ServiceReport.as_view()),name="report_services"),
    path("technician/",login_required(TechnicianReport.as_view()),name="report_technicians"),

]