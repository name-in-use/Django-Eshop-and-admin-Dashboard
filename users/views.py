from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from .models import Users
from django.contrib import messages
from django.template.loader import render_to_string


def User_Login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            #get submitted data from form
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            if name=="" and password =="":
                del request.session['user']
                del request.session['email']
                request.session['user'] = "Guest User"
                request.session['email']=""
                return render(request,'store/store.html')
            else:
                user = Users.objects.filter(name=name, password=password)
                user_email = Users.objects.get(name=name).email

                if user.count() > 0:
                    request.session['user'] = name
                    request.session['email']=user_email
                    
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


def User_Logout(request):
    del request.session['user']
    del request.session['email']
    return redirect("/login/")

