from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('add_employee/', views.add_employee, name='add_employee'),
]