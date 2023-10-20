from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
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