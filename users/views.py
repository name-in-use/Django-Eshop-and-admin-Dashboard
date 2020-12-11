from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.template.loader import render_to_string
from datetime import date

from .forms import LoginForm, RegisterForm
from .models import Users
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist


def User_Login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            # get submitted data from form
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            try:

                user = Users.objects.get(name=name)
                if check_password(password, user.password):

                    request.session['user'] = name
                    request.session['email'] = user.email
                    return redirect("/")
                else:
                    messages.info(request, 'Password is incorect')

            except ObjectDoesNotExist:
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
            # get submitted data from form
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            date_joined = date.today()

            if Users.objects.filter(email=email).exists() and Users.objects.filter(name=name).exists():
                messages.info(request, 'User already exists')
                # return redirect("/register/")
            else:
                user = Users.objects.create(
                    name=name, email=email, date_joined=date_joined)
                user.set_password(password)
                user.save()

                print('user created')
                return redirect("/login/")
        else:
            print(form.errors)

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


def User_Logout(request):
    logout(request)
    response = redirect('/login/')
    response.delete_cookie('cart')
    return response

    del request.session['user']
    del request.session['email']
    # return redirect("/login/")


def User_Profile(request):
    user = request.session['user']
    email = request.session['email']

    
    date_joined = Users.objects.get(name=user).date_joined
    context = {
        'user': user,
        'email': email,
        'date_joined': date_joined
    }
    return render(request, 'users/user_profile.html', context)
