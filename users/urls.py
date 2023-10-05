from django.urls import path
from users.views import AddTechnician , home
urlpatterns = [
    path('', home, name='home'),
    path("add_technician/",AddTechnician.as_view(), name="add_technician")
    
]