from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from .models import Users
from django.contrib import messages
from django.template.loader import render_to_string
from datetime import date

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
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            date_joined=date.today()

            if Users.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                # return redirect("/register/")
            else:
                Users.objects.create(name=name,email=email,password=password,date_joined=date_joined)
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

def User_Profile(request):
    user = request.session['user']
    email = request.session['email']
    
    date_joined = Users.objects.get(name=user).date_joined
    context={
        'user':user,
        'email':email,
        'date_joined':date_joined
    }
    return render(request, 'users/user_profile.html',context)
