from django.contrib import messages
# from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == 'POST':
        username =  request.POST['username']
        email =  request.POST['email']
        password =  request.POST['password']
        password2 =  request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already registered.")
                return redirect("/signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # user_model = User.objects.get(username=username)
                # new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                # new_profile.save()
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')

        return redirect("/signup")
    else:
        return render(request, "signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else: # incorrect password
                messages.info(request, 'Incorrect password')
                return redirect('signin')
        else:
            messages.info(request, 'Incorrect Username')
            return redirect('signin')
    else:
        return render(request, "signin.html")

