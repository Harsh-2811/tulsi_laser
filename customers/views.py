from django.shortcuts import render
from django.urls import reverse_lazy
from customers.forms import MachineTypeForm, CustomerForm, MachineFormSet
from django.views.generic import CreateView, UpdateView, TemplateView, View
from .utils import CustomerInline
# Create your views here.

class AddMachineType(CreateView):
    form_class = MachineTypeForm
    template_name = "add_tech.html"
    success_url = reverse_lazy('add_machine_type')


class AddCustomer(CustomerInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(AddCustomer, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'machines': MachineFormSet(prefix='machines'),
            }
        else:
            return {
                'machines': MachineFormSet(self.request.POST or None, prefix='machines'),
            }
