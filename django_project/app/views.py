from django.views.generic.base import TemplateView
from .forms import UserRegistrationForm, UserLoginForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.views import auth_login, auth_logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.exceptions import (NotAuthenticated, ParseError,
                                       PermissionDenied)


class HomePageView(TemplateView):
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def get_capabilitys(request):
    return render(request, 'capability/capability.html', {})

def login_user(request):
    logout(request)
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                auth_login(request, user)
                return HttpResponseRedirect('/capability')
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
            #check_user_existance
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                auth_login(request, user)
                return HttpResponseRedirect('/capability')
            else:
                raise forms.ValidationError('Looks like a username with that email already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'form' : form})

def check_user_existance(username, email):
    client_email = User.objects.filter(email=email).first()
    client_username = User.objects.filter(username=username).first()
    if (User.objects.filter(username=username, email=email).first()):
        raise PermissionDenied(
            detail='User already exists')
    elif client_email or client_username:
        if client_username:
            raise PermissionDenied(
                detail='This user name has already taken')
        elif client_email:
            raise PermissionDenied(
                detail='This user email has already taken')



def logout_user(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

