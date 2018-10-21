from django.views.generic.base import TemplateView
from .forms import UserRegistrationForm, UserLoginForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import auth_logout
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from app.models import AccessRequest
from django.views.generic.edit import FormView
from .mixin import AjaxFormMixin

class HomePageView(TemplateView):
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



@login_required
def add_access(request):
    return render(request, 'accesses/create_access.html', {})

@login_required
def get_accesses(request):
    user_accesses = AccessRequest.objects.filter(name=request.user.username)
    return render(request, 'accesses/accesses.html', {'accesses' : user_accesses})

def login_user(request):
    logout(request)
    form = UserLoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user is not None :
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/accesses')
    return render(request, 'registration/login.html', {'form' : form})


class RegisterView(AjaxFormMixin, FormView):
    form_class = UserRegistrationForm
    template_name = 'registration/registration.html'
    success_url = '/accesses/'

# class RegisterView(FormView):
#     template_name = 'registration/registration.html'
#     form_class = UserRegistrationForm
#     success_url = "/accesses/"
#
#     def form_valid(self, form):
#         validated_data = form.clean()
#         user = get_user_model().objects.create(
#             username=validated_data['username'],
#             email=validated_data['email']
#         )
#         user.groups.add(Group.objects.get(name='clients'))
#         user.set_password(validated_data['password'])
#         user.save()
#         Token.objects.create(user=user)
#         user_auth = authenticate(username = validated_data['username'],
#                                  password = validated_data['password']
#                                  )
#         login(self.request, user_auth)
#         auth_login(self.request, user_auth)
#
#         return super(RegisterView, self).form_valid(form)


# def register(request):
#     form = UserRegistrationForm(request.POST or None)
#     if request.POST and form.is_valid():
#         userObj = form.clean()
#         username = userObj['username']
#         email =  userObj['email']
#         password =  userObj['password']
#         User.objects.create_user(username, email, password)
#         user = authenticate(username = username, password = password)
#         login(request, user)
#         auth_login(request, user)
#         return HttpResponseRedirect('/accesses')
#     return render(request, 'registration/registration.html', {'form' : form})



def logout_user(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

