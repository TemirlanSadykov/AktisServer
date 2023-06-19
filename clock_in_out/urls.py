from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('clock_in/', views.clock_in_view, name='clock_in'),
    path('clock_out/', views.clock_out_view, name='clock_out'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('register_task_size/', views.register_task_size_view, name='register_task_size'),
    path('start_task_test/', views.start_task_test, name='start_task_test'),
]