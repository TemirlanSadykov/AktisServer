from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from .forms import EmployeeRegistrationForm
from django.views.decorators.csrf import csrf_protect
from .models import Employee, Task, Size, EmployeeTask
from django.http import HttpResponse
from .forms import TaskForm, SizeForm, StartTaskForm

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
        task_values = [item['task'] for item in Task.objects.values('task')]
        response = {'status': 'success', 'tasks': task_values}
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
    return render(request, 'admin_view.html', {'employeetasks': EmployeeTask.objects.all()})

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

def start_task(request):
    csrf_token = get_token(request)

    if request.method == 'POST':
        username = request.POST['employee']
        task = request.POST['task']
        employee = Employee.objects.get(username=username)
        task = Task.objects.get(task=task)
        employee_task = EmployeeTask(employee=employee, task=task)
        employee_task.save()
        response = {'status' : 'success', 'employee_task_id' : employee_task.id}
        return JsonResponse(response)

    return HttpResponse(csrf_token)

def finish_task_test(request):
    csrf_token = get_token(request)

    if request.method == 'POST':
        employee_task_id = request.POST['employee_task_id']
        employee_task = EmployeeTask.objects.get(id = employee_task_id)
        employee_task.set_finish_time()
        response = {'status' : 'success'}
        return JsonResponse(response)

    return HttpResponse(csrf_token)