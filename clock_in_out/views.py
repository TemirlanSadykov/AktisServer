from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .forms import EmployeeRegistrationForm
from django.views.decorators.csrf import csrf_protect
from .models import Employee
from django.http import HttpResponse
import datetime

def login_view(request):

    csrf_token = get_token(request)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        employee = Employee.objects.get(username=username)
        try: 
            if employee.get_authenticated(password):
                # Redirect to a success page
                response = {'status': 'success', 
                            'clock_in_time': getattr(employee, 'clock_in_time'),
                            'clock_out_time': getattr(employee, 'clock_out_time')}
            else:
                # Invalid login credentials, display an error message
                response = {'status': 'error', 'message': 'Invalid Credentials 1'}
        except:
            response = {'status': 'error', 'message': 'Invalid Credentials 2'}

        return JsonResponse(response)

    return HttpResponse(csrf_token)

@csrf_protect
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':'success'})
    else:
        form = EmployeeRegistrationForm()

    return render(request, 'add_employee.html', {'form': form})

def clock_in_view(request):

    csrf_token = get_token(request)
    
    if request.method == 'POST':
        username = request.POST['username']
        employee = Employee.objects.get(username=username)
        employee.set_clock_in_time(datetime.datetime.now())
        response = {'status': 'success', 'message': getattr(employee, 'clock_in_time').strftime('%H:%M:%S')}
        return JsonResponse(response)
        
    return HttpResponse(csrf_token)

def clock_out_view(request):

    csrf_token = get_token(request)
    
    if request.method == 'POST':
        username = request.POST['username']
        employee = Employee.objects.get(username=username)
        employee.set_clock_out_time(datetime.datetime.now())
        response = {'status': 'success', 'message':  getattr(employee, 'clock_out_time').strftime('%H:%M:%S')}
        return JsonResponse(response)
        
    return HttpResponse(csrf_token)
