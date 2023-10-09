from django import forms
from complaints.models import Complain, Payment
from customers.models import Customer
# from searchableselect.widgets import SearchableSelect
class ForeignKeyDatalistWidget(forms.TextInput):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        attrs['list'] = f'list_{name}'
        rendered = super().render(name, value, attrs=attrs, renderer=renderer)
        choices = self.queryset.values_list('pk', 'company_name')
        options = ''.join(f'<option value="{pk}">{name}</option>' for pk, name in choices)
        return f'{rendered}<datalist id="list_{name}">{options}</datalist>'
    
class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = "__all__"
        widgets = {
            'date': forms.DateInput( attrs={'class':'form-control', 'type':'date'}),
            'customer': ForeignKeyDatalistWidget(queryset=Customer.objects.all())
        }
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop('status')

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
            'start_date': forms.DateInput( attrs={'class':'form-control', 'type':'date'}),
            'end_date': forms.DateInput( attrs={'class':'form-control', 'type':'date'}),
            'customer': ForeignKeyDatalistWidget(queryset=Customer.objects.all())
        }
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'