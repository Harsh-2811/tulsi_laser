from customers.models import MachineType, Machine, Customer
from django import forms
from django.forms import inlineformset_factory
class MachineTypeForm(forms.ModelForm):
    class Meta:
        model = MachineType
        fields = "__all__"

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = "__all__"

MachineFormSet = inlineformset_factory(
    Customer, Machine, form=MachineForm,
    extra=1, can_delete=True, can_delete_extra=True
)