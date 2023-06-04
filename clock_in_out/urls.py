from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('get-csrf-token/', views.get_csrf_token, name='get_csfr_token'),
]