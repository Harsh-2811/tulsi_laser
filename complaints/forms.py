from django import forms
from complaints.models import Complain, Payment, Service
from customers.models import Customer
from django.utils import timezone
# from searchableselect.widgets import SearchableSelect
class ForeignKeyDatalistWidget(forms.TextInput):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        attrs['list'] = f'list_{name}'
        rendered = super().render(name, value, attrs=attrs, renderer=renderer)
        choices = self.queryset.values_list('pk', 'company_name')
        options = ''.join(f'<option value="{pk}">{company_name}</option>' for pk, company_name in choices)
        return f'{rendered}<datalist id="list_{name}">{options}</datalist>'
    
class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = "__all__"
        widgets = {
            'date': forms.DateInput( attrs={'class':'form-control', 'type':'date'}),
      
        }
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop('status')
        self.fields['date'].initial = timezone.now().date()
        self.fields['technician'].required = False
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
        widgets = {
            'date': forms.DateInput( attrs={'class':'form-control', 'type':'date'}),
            # 'end_date': forms.DateInput( attrs={'class':'form-control', 'type':'date'}),
            # 'customer': ForeignKeyDatalistWidget(queryset=Customer.objects.all())
        }
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'input_formats': ['%d/%m/%Y']}),
            'completed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'input_formats': ['%d/%m/%Y']}),
        }
        
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop('status')
        self.fields['date'].initial = timezone.now().date()

        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

class ServiceFormCreate(ServiceForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop('completed_date')
        self.fields.pop('completed_by')
