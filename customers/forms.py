from typing import Any
from customers.models import MachineType, Machine, Customer
from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
class MachineTypeForm(forms.ModelForm):
    class Meta:
        model = MachineType
        fields = "__all__"
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop('status')

        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

class EditMachineTypeForm(forms.ModelForm):
    class Meta:
        model = MachineType
        fields = "__all__"
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

class CustomerForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput())
    # name = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Customer
        fields = ("email","company_name","company_mobile_no","manager_name","manager_mobile_no", "accountant_name", "accountant_mobile_no","address")
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'
        

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = "__all__"
        widgets = {
            'purchase_date': forms.DateInput( attrs={'class':'form-control purchase_date'}),
        }
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop('customer')
        self.fields.pop('warranty_end_date')

        self.fields['purchase_date'].initial = timezone.now()
        self.fields['machine_type'].queryset=MachineType.objects.filter(status=MachineType.Statuses.active)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            elif isinstance(visible.field.widget, forms.DateInput):
                visible.field.widget.attrs['class'] = 'form-control purchase_date'

            else:
                visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit: bool = ...) -> Any:
        self.instance.warranty_end_date =(self.instance.purchase_date + timezone.timedelta(days=(self.instance.notify_on * 30)))
        return super().save(commit)

MachineFormSet = inlineformset_factory(
    Customer, Machine, form=MachineForm,
    extra=0, can_delete=True, can_delete_extra=True
)