from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/dashboard/')

    return render(request, 'login.html')

def dashboard_redirect(request):
    if not hasattr(request.user, 'userprofile'):
        return redirect('/admin/')

    role = request.user.userprofile.role

    if role == 'ADMIN':
        return redirect('/admin-dashboard/')
    elif role == 'HR':
        return redirect('/hr-dashboard/')
    elif role == 'EMPLOYEE':
        return redirect('/employee-dashboard/')