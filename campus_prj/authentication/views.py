from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User


def register_page(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, f'Виникла помилка: {form.errors} під час реєстрації')
    return render(request, 'authentication/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Виникла помилка під час авторизації, спробуйте ще раз')
    return render(request, 'authentication/login.html', {})


@login_required
def logout_page(request):
    logout(request)
    return redirect('main')
