from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import EmployeeLoginForm
from .forms import EmployeeForm
from django.views.decorators.csrf import csrf_protect

def login_view(request):

    csrf_token = get_token(request)
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')
        employee = authenticate(request, username=employee_id, password=password)

        if employee is not None:
            response = {'status': 'success', 'message': 'Successful login'}
        else:
            response = {'status': 'error', 'message': 'Invalid Credentials'}
            
        return JsonResponse(response)

    return HttpResponse(csrf_token)

@csrf_protect
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.username = employee.employee_id  # Set employee_id as the username
            employee.save()
            return JsonResponse({'status':'success'})  # Replace 'employee_list' with your desired URL after successful addition
    else:
        form = EmployeeForm()

    return render(request, 'add_employee.html', {'form': form})
