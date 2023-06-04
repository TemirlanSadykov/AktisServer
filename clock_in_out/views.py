from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import HttpResponse

def get_csrf_token(request):
    # Generate a CSRF token
    csrf_token = get_token(request)
    
    # Return the CSRF token as a plain text response
    return HttpResponse(csrf_token)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Perform authentication logic here, e.g., check against a database
        if username == 'admin' and password == 'password':
            response = {'status': 'success', 'message': 'Login successful'}
        else:
            response = {'status': 'error', 'message': 'Invalid credentials'}
            
        return JsonResponse(response)

    return render(request, 'login.html')