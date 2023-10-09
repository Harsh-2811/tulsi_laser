from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib import messages
from .models import Complain, Payment
from django.http import HttpResponseRedirect
from customers.models import Machine, Customer
from complaints.forms import ComplainForm, PaymentForm
# Create your views here.
class Complaints(CreateView, ListView):
    form_class = ComplainForm
    template_name = "add_data_form.html"
    context_object_name = "complaints"
    success_url = reverse_lazy('complaints')
    queryset = Complain.objects.all().order_by('-created_at').exclude(status = Complain.Statuses.completed)

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


class EditComplain(UpdateView):
    form_class = ComplainForm
    template_name = "add_data_form.html"
    success_url = reverse_lazy('complaints')
    queryset = Complain.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Update Complaint" 
        return context

    def form_valid(self, form):
        messages.success(self.request, "Complaint Updated successfully!!!")
        return super().form_valid(form)


class DeleteComplain(DeleteView):
    model = Complain
    context_object_name = 'object'
    success_url = reverse_lazy('complaints')
    template_name = "delete_confirm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_url"] =  reverse_lazy('complaints')
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()

        messages.success(self.request, "Complaint was deleted successfully.")
        return HttpResponseRedirect(success_url)
    

# --------


class Payments(CreateView, ListView):
    form_class = PaymentForm
    template_name = "add_data_form.html"
    context_object_name = "payments"
    success_url = reverse_lazy('payments')
    queryset = Payment.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add Payment" 
        context["table_title"] = "Payments" 
        context["show_lists"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Payment added successfully!!!")
        return super().form_valid(form)

class EditPayment(UpdateView):
    form_class = PaymentForm
    template_name = "add_data_form.html"
    success_url = reverse_lazy('payments')
    queryset = Payment.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Update Payment" 
        return context

    def form_valid(self, form):
        messages.success(self.request, "Payment Updated successfully!!!")
        return super().form_valid(form)


class DeletePayment(DeleteView):
    model = Payment
    context_object_name = 'object'
    success_url = reverse_lazy('payments')
    template_name = "delete_confirm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_url"] =  reverse_lazy('payments')
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()

        messages.success(self.request, "Payment was deleted successfully.")
        return HttpResponseRedirect(success_url)