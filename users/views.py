from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from .models import Users
from django.contrib import messages


def User_Login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            #get submitted data from form
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(email, password)

            user = Users.objects.filter(email=email, password=password)
            if user.count() > 0:
                return redirect("/")

            else:
                messages.info(request, 'Invalid credentials')
                return redirect("/login/")

    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)


def User_Register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            #get submitted data from form
            email = form.cleaned_data.get('email')
            if Users.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                # return redirect("/register/")
            else:
                Users.objects.create(**form.cleaned_data)
                print('user created')
                return redirect("/login/")
        else:
            print(form.errors)

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)
