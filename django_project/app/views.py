from django.views.generic.base import TemplateView
from .forms import UserRegistrationForm, UserLoginForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.views import auth_login, auth_logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
    form = UserLoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user is not None :
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/capability')
    return render(request, 'registration/login.html', {'form' : form})


def register(request):
    form = UserRegistrationForm(request.POST or None)
    if request.POST and form.is_valid():
        userObj = form.clean()
        username = userObj['username']
        email =  userObj['email']
        password =  userObj['password']
        User.objects.create_user(username, email, password)
        user = authenticate(username = username, password = password)
        login(request, user)
        auth_login(request, user)
        return HttpResponseRedirect('/capability')
    return render(request, 'registration/registration.html', {'form' : form})



def logout_user(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

