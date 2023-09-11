from .forms import Videoform
from .models import Profile, Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

@login_required(login_url='/signup/')
def index(request):
    try:
        user = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        user_profile = Profile(user=request.user)

    context = {'user_profile':user_profile}

    return render(request, "index.html", context=context)

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
                # Save user and Profile and redirect to settings page
                user = User.objects.create_user(username=username, email=email, password=password) # type: ignore
                user.save() # Save user as user
                new_profile = Profile.objects.create(user=user, id_user=user.id) # type: ignore
                new_profile.save() # Save User as profile

                login(request, user)
                messages.info(request, 'You are not logged in!')
                return redirect('/settings/')
        else:
            messages.info(request, 'Password not matching')

        return redirect("/signup")
    else:
        return render(request, "signup.html")

@csrf_protect
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

@login_required(login_url='/signin/')
def logoutUser(request):
    logout(request)
    messages.info(request,"You have been successfully logged out.")
    return redirect('signin')

@login_required(login_url='/signin/')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        # Check if 'image' key exists in request.FILES before accessing it
        if 'image' in request.FILES:
            user_profile.proflieImg = request.FILES['image']
        user_profile.bio = request.POST['bio']
        user_profile.location = request.POST['location']
        user_profile.save()

    context = {
    'user_profile': user_profile,
    }
    return render(request, 'setting.html', context=context)

def upload_video(request):
    if request.method == 'POST':
        form = Videoform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Got the video')
    else:
        form = Videoform()
    return render(request, 'upload_form.html', {'form': form})

@login_required(login_url='/signin/') # type: ignore
def post(request):
    correct_user = Post.objects.filter(uploader='rtsfg')
    print(correct_user)
    if request.method == 'POST':
        if 'image_upload' in request.FILES:
            print("image_upload present", request.FILES['image_upload'])
        if 'image_upload' in request.FILES:
            caption = request.POST['caption']
            new_post = Post.objects.create(image=request.FILES['image_upload'], captions=caption, user=request.user)
            new_post.save()
            print('HEll yeah, saving')
            return redirect('/home')
        else:
            print('LOL- FUCK YOU!!!')
    else:
        print("biatch!!! ")
        return redirect('/home/')
