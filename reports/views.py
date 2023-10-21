from django.views.generic import FormView, ListView
from .forms import ComplainReportForm, MachineReportForm, PaymentReportForm
from complaints.models import ComplainOutcome, Payment
from customers.models import Machine
from django.urls import reverse_lazy
import django_filters
from django_filters.views import FilterView
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
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        customer = data.get('customer')
        machine = data.get('machine')
        water_filter = data.get('water_filter')
        alignment = data.get('alignment')
        type_value = data.get('type_value')

        complaint_outcomes = ComplainOutcome.objects.all()
        if customer:
            complaint_outcomes = complaint_outcomes.filter(complain__customer_id = int(customer)).select_related('complain')
        
        if machine:
            complaint_outcomes = complaint_outcomes.filter(complain__machine_id = int(machine)).select_related('complain')

        if start_date and end_date:
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
                    "show_lists":True
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