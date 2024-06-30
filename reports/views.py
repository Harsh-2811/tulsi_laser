from django.views.generic import FormView, ListView
from .forms import ComplainReportForm, MachineReportForm, PaymentReportForm, ServiceReportForm, TechnicianReportForm
from complaints.models import ComplainOutcome, Payment, Service
from customers.models import Machine
from django.urls import reverse_lazy
import django_filters
from django_filters.views import FilterView
from django.db.models import Q
import datetime

# Create your views here.

class ComplainOutcomeFilter(django_filters.FilterSet):
    class Meta:
        model = ComplainOutcome
        fields = ['complaint_type']

class ComplaintReport(FormView, ListView):
    form_class = ComplainReportForm
    template_name = "reports.html"
    success_url = reverse_lazy('report_complaints')
    model = ComplainOutcome
    
    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Complaint Reports" 
        context["table_title"] = "Complaints" 
        context["statuses"] = ComplainOutcome.Complaint_types.choices
        context["filter_url"] = reverse_lazy('report_complaints')
        return context
    
    def form_valid(self, form):
        # You can update the context here
        context = self.get_context_data()
        data = self.request.POST
        complain_id = data.get('complain_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        customer = data.get('customer')
        technician = data.get('technician')
        machine = data.get('machine')
        water_filter = data.get('water_filter')
        alignment = data.get('alignment')
        type_value = data.get('type_value')

        print(data)
        complaint_outcomes = ComplainOutcome.objects.all()
        read_only = False
        if complain_id:
            complaint_outcomes = complaint_outcomes.filter(complain__id = int(complain_id)).select_related('complain')
            read_only = True
        if customer:
            print("Customer", customer)
            complaint_outcomes = complaint_outcomes.filter(complain__customer_id = int(customer)).select_related('complain')
            print(complaint_outcomes)
        if machine:
            print("Machine", machine)
            complaint_outcomes = complaint_outcomes.filter(complain__machine_id = int(machine)).select_related('complain')
            print(complaint_outcomes)
        
        if technician:
            complaint_outcomes = complaint_outcomes.filter(complain__technician_id = int(technician)).select_related('complain')

        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            complaint_outcomes = complaint_outcomes.filter(complain__date__range = (start_date, end_date)).select_related('complain')

        if water_filter:
            complaint_outcomes = complaint_outcomes.filter(water_filter = True)
        
        if alignment:
            complaint_outcomes = complaint_outcomes.filter(alignment = True)

        if type_value:
            complaint_outcomes = complaint_outcomes.filter(complaint_type = type_value)

        context['complaint_outcomes'] = complaint_outcomes
        
        
        context.update(
                {
                    "show_lists":True,
                    "read_only": read_only
                }
            )
        return self.render_to_response(context)
    

class MachineTypeReport(FormView, ListView):
    form_class = MachineReportForm
    template_name = "reports.html"
    success_url = reverse_lazy('report_machine_types')
    model = Machine
    
    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Machine Type Reports" 
        context["table_title"] = "Machines" 
        context["single_field"] = True
        return context
    
    def form_valid(self, form):
        # You can update the context here
        context = self.get_context_data()
        data = self.request.POST
        machine_type = data.get('machine_type')
        machines = []
        if machine_type:
            machines = Machine.objects.filter(machine_type = machine_type)
        context['machines'] = machines
        context.update(
                {
                    "show_lists":True
                }
            )
        return self.render_to_response(context)
    

class PaymentReport(FormView, ListView):
    form_class = PaymentReportForm
    template_name = "reports.html"
    success_url = reverse_lazy('report_payment')
    model = Payment
    
    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Payment Reports" 
        context["table_title"] = "Payments" 
        context["single_field"] = True
        return context
    
    def form_valid(self, form):
        # You can update the context here
        context = self.get_context_data()
        data = self.request.POST
        customer = data.get('customer')
        machines = []
        if customer:
            payments = Payment.objects.filter(customer = customer)
        context['payments'] = payments
        context.update(
                {
                    "show_lists":True
                }
            )
        return self.render_to_response(context)

class ServiceReport(FormView, ListView):
    form_class = ServiceReportForm
    template_name = "reports.html"
    success_url = reverse_lazy('report_services')
    model = Service
    
    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Service Reports" 
        context["table_title"] = "Services" 
        # context["statuses"] = Service.Statuses.choices
        context["filter_url"] = reverse_lazy('report_services')
        return context
    
    def form_valid(self, form):
        # You can update the context here
        context = self.get_context_data()
        data = self.request.POST
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        customer = data.get('customer')
        machine = data.get('machine')

        type_value = data.get('type_value')

        services = Service.objects.all().exclude(status =Service.Statuses.active)
        if customer:
            services = services.filter(customer_id = int(customer)).select_related('customer')
        
        if machine:
            services = services.filter(machine_id = int(machine)).select_related('machine')
        
        if start_date and end_date:
            services = services.filter(solution_date__range = (start_date, end_date))

        if type_value:
            services = services.filter(status = type_value)
        context['services'] = services
        
        
        context.update(
                {
                    "show_lists":True
                }
            )
        return self.render_to_response(context)
    
class TechnicianReport(FormView, ListView):
    form_class = TechnicianReportForm
    template_name = "reports.html"
    success_url = reverse_lazy('report_technicians')
    model = Service
    
    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Technician Reports" 
        context["table_title"] = "Technicians" 
        # context["statuses"] = Service.Statuses.choices
        context["filter_url"] = reverse_lazy('report_technicians')
        return context
    
    def form_valid(self, form):
        # You can update the context here
        context = self.get_context_data()
        data = self.request.POST
        technician = data.get('technician')
        report_type = data.get('report_type')

        if report_type == "Complains":
            complaint_outcomes = ComplainOutcome.objects.filter(technician_id = technician)
            context['complaint_outcomes'] = complaint_outcomes
        else:
            services = Service.objects.filter(Q(completed_by_id = technician) | Q(technician_id = technician)).distinct()
            context['services'] = services

        
        
        context.update(
                {
                    "show_lists":True
                }
            )
        return self.render_to_response(context)
