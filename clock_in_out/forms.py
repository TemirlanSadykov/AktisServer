from django import forms
from .models import Employee
from .models import Task, Size, EmployeeTask

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

class StartTaskForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label=None, to_field_name='username')
    task = forms.ModelChoiceField(queryset=Task.objects.all(), empty_label=None, to_field_name='task')

    class Meta:
        model = EmployeeTask
        fields = ['employee', 'task']
