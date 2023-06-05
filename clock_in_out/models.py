from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    username = models.CharField(max_length=150, unique=True)  # Use employee_id as username
    employee_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    clock_in_time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)

    #Specify a unique related_name for the groups field
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='employee_set',  # Change 'employee_set' to your desired related name
        blank=True,
    )

    # Specify unique related_name arguments for the user_permissions field
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='employee_set',  # Change 'employee_set' to your desired related name
        blank=True,
    )

    def __str__(self):
        return f'{self.employee_id} - {self.username}'
    