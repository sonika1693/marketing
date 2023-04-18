from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from guest_user.decorators import allow_guest_user
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import *


@allow_guest_user
def GuestLogin(request):
    assert request.user.is_authenticated
    return redirect("/content")

@csrf_exempt
def UserLogin(request):
    if request.method == 'GET':
        return render(request, 'UserLogin.html')
    else:
        username = request.POST.get("UserName")
        password = request.POST.get("Password")
        # remember = request.POST.get('remember_me')
        # user = None
        user = auth.authenticate(request, username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            auth.login(request, user)
            # if remember:
            #     settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
            return redirect('content/')
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, 'Incorrect Password')
                return redirect('/')
            except User.DoesNotExist:
                messages.error(request, 'Incorrect Username')
                return redirect('/')

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # next = request.POST.get('next')
        # print(next)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = auth.authenticate(request, username=user.username, password=raw_password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                auth.login(request, user)
                try:
                    next = request.POST.get('next')
                    return redirect(next)
                except:
                    return redirect('/content')
    else:
        form = SignUpForm()
        next = request.GET.get('next')

    return render(request, 'signup.html', {'form': form,'next':next})

def Userlogout(request):
    try:
        request.user.auth_token.delete()
    except Exception as e:
        pass
    auth.logout(request)
    messages.success(request, 'Logged Out Successfully')
    return redirect('/')




# def register(request):
    # if request.method == 'POST':
    #     form = UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         userObj = form.cleaned_data
    #         username = userObj['username']
    #         email =  userObj['email']
    #         password =  userObj['password']
    #         if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
    #             User.objects.create_user(username, email, password)
    #             user = authenticate(username = username, password = password)
    #             login(request, user)
    #             return HttpResponseRedirect('/')
    #         else:
    #             raise forms.ValidationError('Looks like a username with that email or password already exists')

    # else:
    #     form = UserRegistrationForm()

    # return render(request, '/register.html')
