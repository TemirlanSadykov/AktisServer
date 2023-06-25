from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EmployeeRegistrationForm
from django.views.decorators.csrf import csrf_protect
from .models import Employee, Task, EmployeeTask, EmployeeDayResult
from django.http import HttpResponse
from .forms import TaskForm
import datetime
from .scheduler import start_scheduler

def main(request):
    start_scheduler()
    return render(request, 'main.html', {'day': datetime.date.today()})

def login_view(request):

    csrf_token = get_token(request)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        employee = Employee.objects.get(username=username)
        task_values = [item['task'] for item in Task.objects.values('task')]
        try: 
            if employee.get_authenticated(password):
                # Redirect to a success page
                response = {'status': 'success', 'working_task':  getattr(employee, 'working_task'),
                            'clock_in_time': getattr(employee, 'clock_in_time').strftime("%H:%M:%S"),
                            'clock_out_time': getattr(employee, 'clock_out_time').strftime("%H:%M:%S"),
                            'is_active': getattr(employee, 'is_active'), 'tasks': task_values}
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
        response = {'status': 'success'}
        return JsonResponse(response)
        
    return HttpResponse(csrf_token)

def admin_view(request):
    return render(request, 'admin_view.html', {'employees': Employee.objects.all()})

def employee_info(request, arg):
    employee = Employee.objects.get(id=arg)
    employee_tasks = EmployeeTask.objects.filter(employee=employee)
    return render(request, 'employee_info.html', {'employee_tasks': employee_tasks,
                                                  'employee': employee})

def register_task(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        
        if task_form.is_valid():
            task_form.save()
            return JsonResponse({'status': 'success'})
    else:
        task_form = TaskForm()
    
    context = {
        'task_form': task_form,
    }
    return render(request, 'register_task_size.html', context)

def start_task(request):
    csrf_token = get_token(request)

    if request.method == 'POST':
        username = request.POST['employee']
        task = request.POST['task']
        employee = Employee.objects.get(username=username)
        task_to_save = Task.objects.get(task=task)
        employee_task = EmployeeTask(employee=employee, task=task_to_save, start_time = datetime.datetime.now() + datetime.timedelta(hours=6))
        employee_task.save()
        employee.set_working_task(task)
        response = {'status' : 'success', 'employee_task_id' : employee_task.id}
        return JsonResponse(response)

    return HttpResponse(csrf_token)

def finish_task(request):
    csrf_token = get_token(request)

    if request.method == 'POST':
        employee_task_id = request.POST['employee_task_id']
        employee_task = EmployeeTask.objects.get(id = employee_task_id)
        employee_task.set_finish_time()
        response = {'status' : 'success'}
        employee = Employee.objects.get(id = employee_task.employee.id)
        employee.reset_working_task()
        return JsonResponse(response)

    return HttpResponse(csrf_token)

def delete_employee(request, pk):
    employee = Employee.objects.get(pk=pk)
    if request.method == 'POST':
        employee.delete()
        return JsonResponse({'status' : 'success'})
    
    return redirect('admin_view')
    
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return JsonResponse({'status' : 'success'})
    else:
        form = EmployeeRegistrationForm(instance=employee)

    return render(request, 'edit_employee.html', {'form': form})

def daily_report(request):

    if request.method == 'POST':
        date = request.POST['date']
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        return render(request, 'daily_report.html', {'daily_report': EmployeeDayResult.objects.filter(day = date_obj)})