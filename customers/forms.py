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
        fields = ("email","company_name","company_mobile_no","manager_name","manager_mobile_no","address")
    
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
            'purchase_date': forms.DateInput( attrs={'class':'form-control', 'type':'date'}),
        }
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop('customer')
        self.fields['purchase_date'].initial = timezone.now()
        self.fields['machine_type'].queryset=MachineType.objects.filter(status=MachineType.Statuses.active)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

MachineFormSet = inlineformset_factory(
    Customer, Machine, form=MachineForm,
    extra=1, can_delete=True, can_delete_extra=True
)