from django.urls import path
from users.views import AddTechnician
urlpatterns = [
    path("add_technician/",AddTechnician.as_view(), name="add_technician")
]