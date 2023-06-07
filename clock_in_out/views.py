from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .forms import EmployeeRegistrationForm
from django.views.decorators.csrf import csrf_protect
from .models import Employee
from django.http import HttpResponse

def login_view(request):

    csrf_token = get_token(request)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try: 
            if Employee.objects.get(username=username).get_authenticated(password):
                # Redirect to a success page
                response = {'status': 'success', 'message': 'Successful login'}
            else:
                # Invalid login credentials, display an error message
                response = {'status': 'error', 'message': 'Invalid Credentials'}
            return JsonResponse(response)
        except:
            response = {'status': 'error', 'message': 'Invalid Credentials'}
            return JsonResponse(response)

    return HttpResponse(csrf_token)

@csrf_protect
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':'success'})  # Replace 'employee_list' with your desired URL after successful addition
    else:
        form = EmployeeRegistrationForm()

    return render(request, 'add_employee.html', {'form': form})
