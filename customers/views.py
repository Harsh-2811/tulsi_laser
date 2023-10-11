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


from rest_framework import generics, status
from rest_framework.response import Response
from complaints.models import Complain
from .serializers import ComplainSerializer

class ComplainCreateView(generics.CreateAPIView):
    queryset = Complain.objects.all()
    serializer_class = ComplainSerializer

class ComplainUpdateView(generics.UpdateAPIView):
    queryset = Complain.objects.all()
    serializer_class = ComplainSerializer

class ComplainRetrieveView(generics.RetrieveAPIView):
    queryset = Complain.objects.all()
    serializer_class = ComplainSerializer
