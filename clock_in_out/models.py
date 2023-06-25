from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field must be set")
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    clock_in_time = models.DateTimeField(default=datetime.datetime(2020, 3, 1, 0, 0))
    clock_out_time = models.DateTimeField(default=datetime.datetime(2020, 3, 1, 0, 0))
    working_task = models.CharField(max_length=150, default=None, null=True)
    name = models.CharField(max_length=150, default=None, null=True)

    # Additional fields can be added here

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_authenticated(self, password):
        if self.password == password:
            return True
        else:
            return False

    def __str__(self):
        return self.username
    
    def set_clock_in_time(self):
        self.clock_in_time = datetime.datetime.now() + datetime.timedelta(hours=6)
        self.is_active = True
        self.save()

    def set_clock_out_time(self):
        self.clock_out_time = datetime.datetime.now() + datetime.timedelta(hours=6)
        self.is_active = False
        self.save()

    def set_working_task(self, task):
        self.working_task = task
        self.save()

    def reset_working_task(self):
        self.working_task = None
        self.save()
    

class Task(models.Model):
    task = models.CharField(max_length=128)

    def __str__(self):
        return self.task
    
class EmployeeTask(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.employee.username} - {self.task.task}"

    def set_finish_time(self):
        self.finish_time = datetime.datetime.now() + datetime.timedelta(hours=6)
        self.save()

class EmployeeDayResult(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    day = models.DateField(null=True)
    working_hours = models.IntegerField(null=True)
    resting_hours = models.IntegerField(null=True)
    clock_in_time = models.DateTimeField(null=True)
    clock_out_time = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.day} - {self.employee.username}"