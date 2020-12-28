from django.contrib.auth import authenticate, login, forms, logout
from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import UserLoginForm


def login_view(request):
    form=UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, username=email, password=password)
        login(request, user)
        return redirect ('home')
    return render(request, 'accounts/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect ('home')