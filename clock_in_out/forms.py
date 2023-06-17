from django import forms
from .models import Employee
from .models import Task, Size

class EmployeeLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class EmployeeRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['username', 'password']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task']
        labels = {
            'task': 'Task Name'
        }
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control'})
        }

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['size']
        labels = {
            'size': 'Size'
        }
        widgets = {
            'size': forms.TextInput(attrs={'class': 'form-control'})
        }


