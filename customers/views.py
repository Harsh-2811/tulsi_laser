from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from customers.forms import MachineTypeForm, CustomerForm, MachineFormSet, EditMachineTypeForm
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib import messages
from .models import MachineType, Customer, Machine
from django.http import HttpResponseRedirect
from users.models import User
from .utils import CustomerInline
from rest_framework import generics, status
from rest_framework.response import Response
from complaints.models import Complain
from .serializers import ComplainSerializer

# Create your views here.

class MachineTypes(CreateView, ListView):
    form_class = MachineTypeForm
    template_name = "add_data_form.html"
    context_object_name = "machine_types"
    success_url = reverse_lazy('machine_types')
    queryset = MachineType.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add Machine Type" 
        context["single_field"] = True
        context["table_title"] = "Machine Types" 
        context["show_lists"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Machine Type successfully!!!")
        return super().form_valid(form)
    
class EdiMachineType(UpdateView):
    form_class = EditMachineTypeForm
    template_name = "add_data_form.html"
    success_url = reverse_lazy('machine_types')
    queryset = MachineType.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Update Machine Type" 
        return context

    def form_valid(self, form):
        messages.success(self.request, "Technician Updated successfully!!!")
        return super().form_valid(form)


class DeleteMachineType(DeleteView):
    model = MachineType
    context_object_name = 'object'
    success_url = reverse_lazy('machine_types')
    template_name = "delete_confirm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_url"] =  reverse_lazy('machine_types')
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()

        messages.success(self.request, "Technician was deleted successfully.")
        return HttpResponseRedirect(success_url)

 

class AddCustomer(CustomerInline, CreateView):
    template_name = "add_customer.html"
    form_class = CustomerForm
    success_url = reverse_lazy('machine_types')

    def get_context_data(self, **kwargs):
        context = super(AddCustomer, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context["form_title"] = "Add Customer" 
        return context

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'machines': MachineFormSet(prefix='machines'),
            }
        else:
            return {
                'machines': MachineFormSet(self.request.POST or None, prefix='machines'),
            }

    def form_valid(self, form):
        username = self.request.POST['email']
        name = self.request.POST['company_name']
        user = User.objects.create_user(username=username, email=username, first_name=name, password="TulsiLaser@123", role=User.Roles.customer)
        form.instance.user = user
        messages.success(self.request, "Customer added successfully!!!")
        return super().form_valid(form)


class Customers(ListView):
    template_name = "view_customers.html"
    queryset = Customer.objects.all()
    context_object_name = "customers"
    form_class = CustomerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_title"] = "Customers" 
        return context

class EdiCustomers(CustomerInline, UpdateView):
    template_name = "add_customer.html"
    form_class = CustomerForm
    queryset = Customer.objects.all()
    success_url = reverse_lazy('customers')

    def get_context_data(self, **kwargs):
        context = super(EdiCustomers, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context["form_title"] = "Update Customer" 
        # context["allow_first_delete"] = True
        return context

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'machines': MachineFormSet(prefix='machines', instance=self.get_object()),
            }
        else:
            return {
                'machines': MachineFormSet(self.request.POST or None, prefix='machines', instance=self.get_object()),
            }

    def form_valid(self, form):
        username = self.request.POST['email']
        # name = self.request.POST['name']
        form.instance.user.username = username
        form.instance.user.email = username
        form.instance.user.first_name = form.instance.company_name
        form.instance.user.save()
        messages.success(self.request, "Customer Updated successfully!!!")
        return super().form_valid(form)

    def get_initial(self, **kwargs):
        instance = self.get_object(**kwargs)
        return {
            "name": instance.user.first_name,
            "email": instance.user.email,
        }


class DeleteCustomers(DeleteView):
    model = Customer
    context_object_name = 'customer'
    success_url = reverse_lazy('customers')
    template_name = "delete_confirm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_url"] =  reverse_lazy('customers')
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        self.object.user.delete()
        messages.success(self.request, "Customer was deleted successfully.")
        return HttpResponseRedirect(success_url)

class ComplainCreateView(generics.CreateAPIView):
    queryset = Complain.objects.all()
    serializer_class = ComplainSerializer

class ComplainUpdateView(generics.UpdateAPIView):
    queryset = Complain.objects.all()
    serializer_class = ComplainSerializer

class ComplainRetrieveView(generics.RetrieveAPIView):
    queryset = Complain.objects.all()
    serializer_class = ComplainSerializer

class Machines(ListView):
    template_name = "machines.html"
    context_object_name = "machines"
    queryset = Machine.objects.all().order_by('-created_at')

    def get_queryset(self) -> QuerySet[Any]:
        if 'customer' in self.request.GET:
            customer = self.request.GET['customer']
            self.queryset = self.queryset.filter(customer_id = int(customer))
        
        return self.queryset