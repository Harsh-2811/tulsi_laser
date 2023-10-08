from django import forms
from complaints.models import Complain
from searchableselect.widgets import SearchableSelect
class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = "__all__"
        widgets = {
            'date': forms.DateInput( attrs={'class':'form-control', 'type':'date'}),
            #  'machine': SearchableSelect(model='customers.Machine', search_field='code', limit=10)
        }
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop('status')

        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'