from django import forms
from .models import Employee

class LoginForm(forms.Form):
    employee_id = forms.CharField(label='Employee ID', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'employee_id']

class ClockInForm(forms.Form):
    employee = forms.ChoiceField(label='Employee', choices=())

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees', None)
        super().__init__(*args, **kwargs)
        if employees:
            self.fields['employee'].choices = [(employee.id, employee.name) for employee in employees]
