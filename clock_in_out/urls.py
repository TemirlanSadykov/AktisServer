from django.urls import path
from . import views

urlpatterns = [
    path('clock-in/', views.clock_in, name='clock_in'),
    path('clock-out/', views.clock_out, name='clock_out'),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('delete-employee/<str:employee_id>/', views.delete_employee, name='delete_employee'),
]