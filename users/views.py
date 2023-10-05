from django.shortcuts import render
from django.urls import reverse_lazy
from users.forms import TechnicianForm
from users.models import User
from django.views.generic import CreateView, UpdateView, TemplateView, View
# Create your views here.

def home(request):
    # Your view logic here
    return render(request, 'base.html')

class AddTechnician(CreateView):
    form_class = TechnicianForm
    template_name = "add_tech.html"
    success_url = reverse_lazy('add_technician')

    def form_valid(self, form):
        username = self.request.POST['email']
        name = self.request.POST['name']
        user = User.objects.create(username=username, email=username, first_name=name, password="TulsiLaser@123")
        form.instance.user = user
        return super().form_valid(form)