from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from users.models import *
from customers.models import *
# from dal import autocomplete
class TechnicianForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput())
    name = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Technician
        fields = ("email", "name", "phone_1", "phone_2", "expertise", "address", "app_access", "web_access")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # self.fields.pop('user')

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-check-input'
                visible.field.widget.attrs['data_type'] = 'checkbox'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email, username=email).exists():
            raise forms.ValidationError("This email address is already exists. Please supply a different email address.")
        return email

class TechnicianEditForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput())
    name = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Technician
        fields = ("email", "name", "phone_1", "phone_2", "expertise", "address", "app_access", "web_access")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # self.fields.pop('user')

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-check-input'
                visible.field.widget.attrs['data_type'] = 'checkbox'
    

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if User.objects.filter(username = username).exists():
            user = User.objects.get(username = username)
            if not user.is_superuser:
                print("User Details : ",user)
                if Technician.objects.filter(user = user).exists():
                    tech = Technician.objects.get(user = user)
                    print("technicial objects 1: ",tech)
                    if not tech.web_access:
                        print("technicial objects 2: ")
                        raise forms.ValidationError("You not have permission for this platform")
                else:
                    
                    raise forms.ValidationError("You not have permission for this platform")
        return super().clean()