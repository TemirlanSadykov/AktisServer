from django.http import JsonResponse

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

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})