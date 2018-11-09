from django.views.generic.base import TemplateView
from .forms import UserRegistrationForm, UserLoginForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.views import auth_logout
from django.contrib.auth.decorators import login_required
from app.models import AccessRequest
from django.views.generic.edit import FormView
from .mixin import AjaxRegistrationMixin, AjaxLoginMixin
from django.views.generic import ListView
from app.helpers import paginator_work

class HomePageView(TemplateView):
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@login_required
def add_access(request):
    if request.POST:
        name = request.POST['username']
        space_name = request.POST['space_name']
        AccessRequest.objects.create(name=name, space_name=space_name)
        return HttpResponseRedirect('/accesses')
    return render(request, 'accesses/create_access.html', {})

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
            paginator = paginator_work(self.request, qs, 1)
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

class AccessDetail(ListView):
    context_object_name = 'access'
    template_name = 'accesses/edit_access.html'

    def get_queryset(self):
        self.access = get_object_or_404(AccessRequest, id=self.kwargs['pk'])
        return self.access

