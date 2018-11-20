from django.views.generic.base import TemplateView
from .forms import UserRegistrationForm, UserLoginForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.views import auth_logout
from app.models import AccessRequest
from django.views.generic.edit import FormView
from .mixin import AjaxRegistrationMixin, AjaxLoginMixin
from django.views.generic import ListView, UpdateView, CreateView
from app.helpers import paginator_work
from app.forms import CreateAccessForm, EditAccessForm


class HomePageView(TemplateView):
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AccessesCreate(CreateView):
    form_class = CreateAccessForm
    template_name = 'accesses/create_access.html'
    success_url = '/accesses'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.name = self.request.user
        instance.save()
        return redirect(self.success_url)


class AccessesList(ListView):
    template_name = "accesses/accesses.html"
    model = AccessRequest

    def get_context_data(self, **kwargs):
        qs = self.model.objects.all()
        if qs.exists():
            list_groups = []
            for g in self.request.user.groups.all():
                list_groups.append(g.name)
            if 'managers' in list_groups:
                qs = self.model.objects.all()
            else:
                qs = self.model.objects.filter(name=self.request.user.username)
            paginator = paginator_work(self.request, qs, 5)
            params = self.request.GET.copy()
            if 'page' in params:
                del params['page']
            context = {
                'paginator': paginator['paginator'],
                'accesses': paginator['page_objects'],
            }
        else:
            context = {}
        return context

class RegisterView(AjaxRegistrationMixin, FormView):
    form_class = UserRegistrationForm
    template_name = 'registration/registration.html'
    success_url = '/accesses/'

class LoginView(AjaxLoginMixin, FormView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    success_url = '/accesses/'

def logout_user(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

class AccessEdit(UpdateView):
    model = AccessRequest
    context_object_name = 'access'
    form_class = EditAccessForm
    template_name = 'accesses/edit_access.html'
    success_url = '/accesses'
