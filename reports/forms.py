from django import forms
from complaints.models import Complain, Payment, Service
from customers.models import Machine
from users.models import Technician
class ComplainReportForm(forms.ModelForm):
    start_date = forms.DateField(
        
    )
    end_date = forms.DateField(
        
    )
    water_filter = forms.BooleanField(widget=forms.CheckboxInput())
    alignment = forms.BooleanField(widget=forms.CheckboxInput())
    class Meta:
        model = Complain
        fields = ('customer', 'machine', 'start_date', 'end_date', 'technician')
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            elif isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-check-input'
                visible.field.widget.attrs['data_type'] = 'checkbox'

               
            else:
                visible.field.widget.attrs['class'] = 'form-control'
            
            visible.field.required = False

class MachineReportForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ('machine_type', )
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = False

class PaymentReportForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('customer', )
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = False


class ServiceReportForm(forms.ModelForm):
    start_date = forms.DateField(
    
    )
    end_date = forms.DateField(
       
    )
    class Meta:
        model = Service
        fields = ('customer', 'machine', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            elif isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-check-input'
                visible.field.widget.attrs['data_type'] = 'checkbox'

               
            else:
                visible.field.widget.attrs['class'] = 'form-control'
            
            visible.field.required = False

class TechnicianReportForm(forms.Form):

    technician = forms.ModelChoiceField(queryset=Technician.objects.all())
    report_type = forms.ChoiceField(choices=[("Complains", "Complains"), ("Service", "Service and Support")])

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            elif isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-check-input'
                visible.field.widget.attrs['data_type'] = 'checkbox'

               
            else:
                visible.field.widget.attrs['class'] = 'form-control'
            
            visible.field.required = False