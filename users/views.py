from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.urls import reverse_lazy
from users.forms import TechnicianForm
from users.models import User, Technician, APKs
from django.views.generic import CreateView, UpdateView, TemplateView, View, ListView, DeleteView
from django.contrib import messages
from django.http import HttpResponseRedirect
from customers.models import Customer, Machine, MachineType
from complaints.models import Complain
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
# Create your views here.

@login_required()
def home(request):
    # Your view logic here
    total_customers = Customer.objects.count()
    total_machines = Machine.objects.all()
    todays_complaints = Complain.objects.filter(date=timezone.now().date()).count()
    this_month_complaints = Complain.objects.filter(date__month=timezone.now().date().month).count()
    machine_types = MachineType.objects.count()
    complaints = Complain.objects.filter(date=timezone.now().date()).order_by('-created_at')

    current_month = datetime.today().month
    prev_month = (datetime.today() - timedelta(days=30)).month
    current_year = datetime.today().year

    ending_months = Machine.objects.filter(
                              warranty_end_date__year__gte=current_year,
                              warranty_end_date__month__gte=prev_month,
                              warranty_end_date__year__lte=current_year,
                              warranty_end_date__month__lte=current_month)
    print(ending_months)
    if 'status' in request.GET:
        if request.GET['status'] != "0":
            complaints = complaints.filter(status = request.GET['status'])
    complaint_statuses = Complain.Statuses.choices
    from_date = ""
    to_date = ""
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        total_machines = total_machines.filter(purchase_date__range = (from_date, to_date))

    return render(request, 'home.html',{"total_customers":total_customers, "total_machines":total_machines, "todays_complaints":todays_complaints, "this_month_complaints":this_month_complaints, "machine_types":machine_types, "complaints":complaints, "complaint_statuses":complaint_statuses, "from_date":from_date, "to_date":to_date, "ending_months": ending_months})

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
        user = User.objects.create_user(username=username, email=username, first_name=name, password="TulsiLaser@123", role=User.Roles.technician)
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
        context["form_title"] = "Update Technician" 
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
    
class APKListing(TemplateView):
    template_name = "machines.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["apks"] =  APKs.objects.all().order_by('-created_at')
        return context

