from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import EmployeeDayResult, EmployeeTask, Employee
import datetime


def save_employee_day_result():
    # Get the current date and time in UTC +6
    now = timezone.now() + timezone.timedelta(hours=6)

    if now.hour == 18 and now.minute == 5:
        employee_day_result = EmployeeDayResult()
        employee_day_result.day = datetime.date.today()
        for id in Employee.objects.values_list('id', flat=True):
            employee = Employee.objects.get(id=id)
            working_hours = 0
            try:
                for employee_task in EmployeeTask.objects.filter(employee=employee):
                    working_hours += employee_task.finish_time - employee_task.start_time
                    employee_task.delete()
            except EmployeeTask.DoesNotExist:
                working_hours = 0
            resting_hours = employee.clock_out_time - employee.clock_in_time - working_hours
            employee_day_result.employee = employee
            employee_day_result.working_hours = working_hours
            employee_day_result.resting_hours = resting_hours
            employee_day_result.clock_in_time = employee.clock_in_time
            employee_day_result.clock_out_time = employee.clock_out_time
            employee_day_result.save()
        employee.clock_in_time = now
        employee.clock_out_time = now


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(save_employee_day_result, 'cron', hour=18, minute=5)
    scheduler.start()