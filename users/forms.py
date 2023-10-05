from typing import Any
from django import forms
from users.models import *
class TechnicianForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput())
    name = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Technician
        fields = ("email", "name", "phone_1", "phone_2", "expertise", "address")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # self.fields.pop('user')

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
