from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.urls import reverse_lazy
from users.forms import TechnicianForm
from users.models import User, Technician
from django.views.generic import CreateView, UpdateView, TemplateView, View, ListView, DeleteView
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    # Your view logic here
    return render(request, 'home.html')

class Technicians(CreateView, ListView):
    form_class = TechnicianForm
    template_name = "add_data_form.html"
    success_url = reverse_lazy('technicians')
    context_object_name = "technicians"
    queryset = Technician.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add Technician" 
        context["table_title"] = "Technicians" 
        context["show_lists"] = True

        return context
    
    def form_valid(self, form):
        username = self.request.POST['email']
        name = self.request.POST['name']
        user = User.objects.create(username=username, email=username, first_name=name, password="TulsiLaser@123")
        form.instance.user = user
        messages.success(self.request, "Technician added successfully!!!")
        return super().form_valid(form)


class EdiTechnician(UpdateView):
    form_class = TechnicianForm
    template_name = "add_data_form.html"
    success_url = reverse_lazy('technicians')
    queryset = Technician.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Udpate Technician" 
        return context

    def form_valid(self, form):
        username = self.request.POST['email']
        name = self.request.POST['name']
        form.instance.user.username = username
        form.instance.user.email = username
        form.instance.user.first_name = name
        form.instance.user.save()

        messages.success(self.request, "Technician Updated successfully!!!")
        return super().form_valid(form)

    def get_initial(self, **kwargs):
        instance = self.get_object(**kwargs)
        return {
            "name": instance.user.first_name,
            "email": instance.user.email,
        }

class DeleteTechnician(DeleteView):
    model = Technician
    context_object_name = 'technician'
    success_url = reverse_lazy('technicians')
    template_name = "delete_confirm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_url"] =  reverse_lazy('technicians')
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        self.object.user.delete()
        messages.success(self.request, "Technician was deleted successfully.")
        return HttpResponseRedirect(success_url)

