from django import forms
from django.contrib.auth.models import User
from .models import CountryList


class UserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())
    country = forms.ModelChoiceField(queryset=CountryList.objects.all())

    class Meta:
        model=User
        fields=['first_name','last_name','email','country','username','password','password2']
        widgets = {
            'password': forms.PasswordInput(),
        }

class InputDataForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=CountryList.objects.all(),required=False)
    Days = forms.IntegerField(required=False)
    class Meta:
        model=CountryList
        fields='__all__'