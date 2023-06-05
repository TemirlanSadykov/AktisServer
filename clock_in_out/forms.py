from django import forms
from .models import Employee
from django.contrib.auth.forms import AuthenticationForm

class EmployeeLoginForm(AuthenticationForm):
    employee_id = forms.CharField(label='Employee ID')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['employee_id', 'password']
