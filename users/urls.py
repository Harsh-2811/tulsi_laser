from django.urls import path
from users.views import Technicians, EdiTechnician, DeleteTechnician
urlpatterns = [
    path("technicians/",Technicians.as_view(), name="technicians"),
    path("technician/edit/<int:pk>/",EdiTechnician.as_view(),name="edit_techician"),
    path("technician/delete/<int:pk>/",DeleteTechnician.as_view(),name="delete_techician"),

]