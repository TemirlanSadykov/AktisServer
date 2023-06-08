from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from enum import Enum

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
    clock_in_time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)
    
    # Additional fields can be added here

    is_active = models.BooleanField(default=True)
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
    
    def set_clock_in_time(self, clock_in):
        self.clock_in_time = clock_in

    def set_clock_out_time(self, clock_out):
        self.clock_out_time = clock_out
    
'''
class Task(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class TaskSize(Enum):
    S42 = '42'
    S44 = '44'
    S46 = '46'
    
class EmployeeTask(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    sizes = models.CharField(
        max_length=20,
        choices=[(tag, tag.value) for tag in TaskSize],
        default=TaskSize.SMALL.value
    )


    def __str__(self):
        return f"{self.employee.username} - {self.task.name}"
'''