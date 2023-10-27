from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from users.models import *
from customers.models import *
from dal import autocomplete
class TechnicianForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput())
    name = forms.CharField(widget=forms.TextInput())
    # machine = forms.ModelChoiceField(
    #     queryset=Machine.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control select2'}),
    # )
    # customer = forms.ModelChoiceField(
    #     queryset=Customer.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control select2'}),
    # )
    

    class Meta:
        model = Technician
        fields = ("email", "name", "phone_1", "phone_2", "expertise", "address")
    
    widgets = {
            'email': autocomplete.ModelSelect2(url='customer-autocomplete')
        }
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # self.fields.pop('user')

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email, username=email).exists():
            raise forms.ValidationError("This email address is already exists. Please supply a different email address.")
        return email
    

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'