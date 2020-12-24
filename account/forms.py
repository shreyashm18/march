from django import forms
from django.contrib.auth.models import User
from .models import CountryList
from django.contrib import messages
from django.shortcuts import render,redirect
from datetime import datetime, timedelta

class UserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())
    country = forms.ModelChoiceField(queryset=CountryList.objects.all())

    class Meta:
        model=User
        fields=['first_name','last_name','email','country','username','password','password2']
        widgets = {
            'password': forms.PasswordInput(),
        }

from rest_framework import exceptions

class InputDataForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=CountryList.objects.all(),required=False)
    # Days = forms.IntegerField(required=False)
    start_date = forms.DateField(required=False,widget = forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date   = forms.DateField(required=False,widget = forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model=CountryList
        fields='__all__'
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        print(f'cleaned data ={cleaned_data}')
        today = datetime.today().date()
        if not end_date == None:
            if end_date <= today:
                if end_date <= start_date:
                    raise forms.ValidationError("End date should be greater than start date.")
            else:
                raise forms.ValidationError("End date should not be greater than today.")
        return self.cleaned_data
