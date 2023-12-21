from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Forms & Models
from App_Login.forms import SignUpForm, ProfileForm
from App_Login.models import Profile

# Messages
from django.contrib import messages

# Create your views here.

def sign_up(request):
    form = SignUpForm()
    # registered = False

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            # registered = True
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse('App_Login:login'))

    # dict = {'form':form, 'registered':registered}
    return render(request, 'App_Login/sign_up.html', context={'form':form})

def login_user(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Shop:home'))

    return render(request, 'App_Login/login.html', context={'form':form})

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, 'You have been logged out')
    return HttpResponseRedirect(reverse('App_Shop:home'))

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            form = ProfileForm(instance=profile)

    return render(request, 'App_Login/change_profile.html', context={'form':form})
