from django.urls import path
from users.views import Technicians, EdiTechnician, DeleteTechnician, APKListing
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm
from . import autocomplete_views

urlpatterns = [
    path("login/",LoginView.as_view(template_name='login.html', form_class = CustomAuthenticationForm), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("technicians/",login_required(Technicians.as_view()), name="technicians"),
    path("technician/edit/<int:pk>/",login_required(EdiTechnician.as_view()),name="edit_techician"),
    path("technician/delete/<int:pk>/",login_required(DeleteTechnician.as_view()),name="delete_techician"),
    path("apks/",login_required(APKListing.as_view()), name="apks")
]
