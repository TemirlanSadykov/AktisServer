from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from .forms import EmployeeRegistrationForm
from django.views.decorators.csrf import csrf_protect
from .models import Employee, Task, Size
from django.http import HttpResponse
from .forms import TaskForm, SizeForm

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
                            'clock_in_time': getattr(employee, 'clock_in_time').strftime("%H:%M:%S"),
                            'clock_out_time': getattr(employee, 'clock_out_time').strftime("%H:%M:%S")}
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
        employee.set_clock_in_time()
        response = {'status': 'success', 
                    'tasks': list(Task.objects.values('name')), 'sizes': list(Size.objects.values('size'))}
        return JsonResponse(response)
        
    return HttpResponse(csrf_token)

def clock_out_view(request):

    csrf_token = get_token(request)
    
    if request.method == 'POST':
        username = request.POST['username']
        employee = Employee.objects.get(username=username)
        employee.set_clock_out_time()
        response = {'status': 'success', 'message':  getattr(employee, 'clock_out_time').strftime('%H:%M:%S')}
        return JsonResponse(response)
        
    return HttpResponse(csrf_token)

def admin_view(request):
    return render(request, 'admin_view.html', {'employees': Employee.objects.all()})

def register_task_size_view(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        size_form = SizeForm(request.POST)
        
        if task_form.is_valid() and size_form.is_valid():
            task_form.save()
            size_form.save()
            return JsonResponse({'status': 'success'})
    else:
        task_form = TaskForm()
        size_form = SizeForm()
    
    context = {
        'task_form': task_form,
        'size_form': size_form,
    }
    return render(request, 'register_task_size.html', context)