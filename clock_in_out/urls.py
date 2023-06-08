from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('clock_in/', views.clock_in_view, name='clock_in'),
    path('clock_out/', views.clock_out_view, name='clock_out'),
]