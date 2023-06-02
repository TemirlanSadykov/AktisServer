from django.db import models

class Task(models.Model):
    start_time = models.TimeField()
    finish_time = models.TimeField()

    def __str__(self):
        return f'{self.start_time} - {self.finish_time}'

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100)
    clock_in_time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)
    total_working_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.employee_id} - {self.name}'

class EmployeeTask(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

