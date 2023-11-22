from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib import messages
from .models import Complain, Payment, Service, ComplainOutcome
from django.http import HttpResponseRedirect, JsonResponse
from customers.models import Machine, Customer
from complaints.forms import ComplainForm, PaymentForm, ServiceForm, ServiceFormCreate
from django.utils import timezone
# Create your views here.

import django_filters
from django_filters.views import FilterView

class ComplaintFilter(django_filters.FilterSet):
    class Meta:
        model = Complain
        fields = ['status']

class ServiceFilter(django_filters.FilterSet):
    class Meta:
        model = Service
        fields = ['status']


class Complaints(CreateView, FilterView):
    form_class = ComplainForm
    template_name = "add_data_form.html"
    context_object_name = "complaints"
    success_url = reverse_lazy('complaints')
    filterset_class = ComplaintFilter
    model = Complain
    queryset = Complain.objects.all().order_by('-created_at').exclude(status = Complain.Statuses.completed)

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add Complaint" 
        context["table_title"] = "Complaints" 
        context["show_lists"] = True
        if self.request.user.role == "technician":
            context["statuses"] = Complain.TechStatuses.choices
        else:
            context["statuses"] = Complain.Statuses.choices
        context["filter_url"] = reverse_lazy('complaints')
        return context
    
    def get_queryset(self):
        if self.request.user.role == "technician":
            queryset = self.queryset.filter(technician = self.request.user.technician)
            return queryset

        return self.queryset

    

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.technician:
            obj.status = Complain.Statuses.pending
        else:
            obj.status = Complain.Statuses.new

        from pyfcm import FCMNotification
        from django.conf import settings

        push_service = FCMNotification(api_key=settings.FCM_TOKEN)
        try:
            result = push_service.notify_single_device(registration_id=obj.technician.user.push_token, message_title="New Complain assigned to you.", message_body=f"Complain for machine {obj.machine.code} of {obj.customer.company_name}")
        except:
            pass
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

def getAddressByCustomer(request):
    cid = request.GET['customer_id']
    customer = Customer.objects.get(id = cid)
    return JsonResponse({"address":customer.address}, safe=False)

def checkIfComplainExistForDay(request, mid):
    is_complain_exits = Complain.objects.filter(machine_id = mid, date = timezone.now().date()).exists()
    return JsonResponse({"is_complain_exits":is_complain_exits}, safe=False)


class EditComplain(UpdateView):
    form_class = ComplainForm
    template_name = "add_data_form.html"
    success_url = reverse_lazy('complaints')
    queryset = Complain.objects.all().order_by('-created_at')
    model = Complain

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Update Complaint" 
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.technician:
            obj.status = Complain.Statuses.pending
        else:
            obj.status = Complain.Statuses.new
        messages.success(self.request, "Complaint Updated successfully!!!")
        return super().form_valid(form)


class DeleteComplain(DeleteView):
    model = Complain
    context_object_name = 'object'
    success_url = reverse_lazy('complaints')
    template_name = "delete_confirm.html"
    
    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
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
    model = Payment

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
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
    model = Payment
    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
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
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["list_url"] =  reverse_lazy('payments')
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()

        messages.success(self.request, "Payment was deleted successfully.")
        return HttpResponseRedirect(success_url)
    

class Services(CreateView, FilterView):
    form_class = ServiceFormCreate
    template_name = "add_data_form.html"
    context_object_name = "services"
    success_url = reverse_lazy('services')
    filterset_class = ServiceFilter
    model = Service
    queryset = Service.objects.all().order_by('-created_at').exclude(status = Service.Statuses.completed)

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add Service" 
        context["table_title"] = "Services" 
        context["show_lists"] = True
        context["statuses"] = Service.Statuses.choices
        context["filter_url"] = reverse_lazy('services')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Service added successfully!!!")
        return super().form_valid(form)
    
    
class EditService(UpdateView):
    form_class = ServiceForm
    template_name = "add_data_form.html"
    success_url = reverse_lazy('services')
    queryset = Service.objects.all().order_by('-created_at')
    model = Service

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Update Service" 
        return context

    def form_valid(self, form):
        service = form.save(commit=False)
        if service.completed_date and service.completed_by:
            service.status = Service.Statuses.completed # Change 'new_status' to your desired status
            service.save()

        messages.success(self.request, "Service Updated successfully!!!")
        return super().form_valid(form)


class DeleteService(DeleteView):
    model = Service
    context_object_name = 'object'
    success_url = reverse_lazy('services')
    template_name = "delete_confirm.html"
    
    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["list_url"] =  reverse_lazy('services')
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()

        messages.success(self.request, "Service was deleted successfully.")
        return HttpResponseRedirect(success_url)
    

def getComplaintOutcomeByMachine(request):
    mid = request.GET['machine_id']
    request_for = request.GET['request_for']
    if request_for == "outcomes":
        outcomes = ComplainOutcome.objects.filter(complain__machine_id = mid).select_related('complain')[:5]
        return render(request, "complain_history.html", {"outcomes":outcomes})
    elif request_for == "services":
        services = Service.objects.filter(machine_id = mid)[:5]
        return render(request, "complain_history.html", {"services":services})
    
def checkIfLimitOver(request):
    mid = request.GET['machine_id']
    machine = Machine.objects.get(id = mid)
    current_month = timezone.now().month
    current_year = timezone.now().year
    if Complain.objects.filter(machine = machine, date__month = current_month, date__year = current_year).count() > machine.complain_limit:
        return JsonResponse({"limit_over": True})
    else:
        return JsonResponse({"limit_over": False})

def updateStatusToRunning(request, id):
    complain = Complain.objects.get(id =id)
    complain.status = Complain.Statuses.running
    complain.save()

    return redirect("complaints")
