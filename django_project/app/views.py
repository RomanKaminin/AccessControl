from django.views.generic.base import TemplateView
from .forms import UserRegistrationForm, UserLoginForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.views import auth_login, auth_logout
from django.contrib.auth import authenticate, login, logout


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def login_user(request):
    logout(request)
    if request.POST:
        form = UserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                auth_login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form' : form})


def register(request):
    if request.POST:
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'form' : form})

def exit(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

