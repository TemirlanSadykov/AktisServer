from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm
from .forms import ClockInForm
import datetime

def employee_clock_in(request):
    if request.method == 'POST':
        form = ClockInForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee']
            employee = Employee.objects.get(id=employee_id)
            employee.clock_in_time = datetime.now()
            employee.save()
            return redirect('clock_in_success')
    else:
        form = ClockInForm()
    employees = Employee.objects.all()
    return render(request, 'employee_clock_in.html', {'form': form, 'employees': employees})

def clock_out(request):
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        employee = Employee.objects.get(id=employee_id)
        employee.clock_out_time = datetime.datetime.now()
        employee.save()
        return redirect('clock_in')
    employees = Employee.objects.filter(clock_out_time__isnull=True)
    return render(request, 'clock_out.html', {'employees': employees})

def admin_view(request):
    employees = Employee.objects.all()
    return render(request, 'admin_view.html', {'employees': employees})

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_view')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

def delete_employee(request, employee_id):
    employee = Employee.objects.get(employee_id=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('admin_view')
    return render(request, 'delete_employee.html', {'employee': employee})