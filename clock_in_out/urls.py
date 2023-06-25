from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login_view, name='login'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('clock_in/', views.clock_in_view, name='clock_in'),
    path('clock_out/', views.clock_out_view, name='clock_out'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('employee_info/<int:arg>', views.employee_info, name='employee_info'),
    path('delete_employee/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('edit_employee/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('register_task/', views.register_task, name='register_task'),
    path('start_task/', views.start_task, name='start_task'),
    path('finish_task/', views.finish_task, name='finish_task'),
    path('daily_report/', views.daily_report, name='daily_report'),
]