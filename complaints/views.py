from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, View, ListView, DeleteView
from django.contrib import messages
from .models import Complain
from django.http import HttpResponseRedirect
from users.models import User
from customers.models import Machine, Customer
from complaints.forms import ComplainForm
# Create your views here.
class Complaints(CreateView, ListView):
    form_class = ComplainForm
    template_name = "add_data_form.html"
    context_object_name = "complaints"
    success_url = reverse_lazy('complaints')
    queryset = Complain.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add Complaint" 
        context["table_title"] = "Complaints" 
        context["show_lists"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Complaint Generated successfully!!!")
        return super().form_valid(form)

def getCompanyByMachine(request):
    mid = request.GET['machine_id']
    customers = Customer.objects.filter(machines__id = mid)
    return render(request, "customers_list.html", {"customers":customers})

def getMachinesByCustomer(request):
    cid = request.GET['customer_id']
    machines = Machine.objects.filter(customer__id = cid)
    return render(request, "machines_list.html", {"machines":machines})