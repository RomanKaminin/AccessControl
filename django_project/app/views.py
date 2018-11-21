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
from django.contrib.auth.models import User
from urllib.parse import urlencode
from django.db.models import Q
from django.conf import settings


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
            paginator = paginator_work(self.request, qs.order_by('-date'), 3)
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

class AlphaList(ListView):
    template_name = 'accesses/alpha_detail.html'
    model = User

    def get_context_data(self, **kwargs):
        qs = self.model.objects.all()
        if qs.exists():
            params = self.request.GET.copy()
            if 'page' in params:
                del params['page']

            values_alph = []
            if 'alph_val' in params:
                alph_literals = params['alph_val'][2:-2].split("-")
                alph_literals.extend(settings.VALUES_ALPH[len(settings.VALUES_ALPH) -
                                                          settings.VALUES_ALPH[::-1].index(alph_literals[0]):
                                                          settings.VALUES_ALPH.index(alph_literals[1])]
                                     )
                qs = self.model.objects.none()
                queryset = self.model.objects.all()

                for i in alph_literals:
                    query_feltred = queryset.order_by("first_name").filter(
                        Q(first_name__startswith=i) | Q(first_name__startswith=i.lower())
                    )
                    qs = qs.union(query_feltred)


            first_names = self.model.objects.all().values_list('first_name')
            first_names_list = [first_name[0][0] for first_name in first_names]
            for item in first_names_list:
                if item.upper() not in values_alph:
                    values_alph.append(item.upper())
            values_alph = sorted(values_alph)

            filters_alph = []
            if len(values_alph) > 4:
                number = 2
                if 4 < len(values_alph) <= 9:
                    number = 2
                elif 9 < len(values_alph) <= 13:
                    number = 3
                elif 13 < len(values_alph) <= 19:
                    number = 4
                elif 19 < len(values_alph) <= 25:
                    number = 5
                elif 25 < len(values_alph) <= 30:
                    number = 6
                elif  len(values_alph) > 30:
                    number = 7
                filter_alph_lists = self.split_alph_list(values_alph, number)
                for item_alph in filter_alph_lists:
                    filters_alph.append(['{}-{}'.format(item_alph[0], item_alph[-1])])
            else:
                filters_alph.append(['{}-{}'.format(values_alph[0], values_alph[-1])])

            if 'number_records' in params:
                number_records = params['number_records']
            else:
                number_records = 5
            paginator = paginator_work(self.request, qs.order_by('first_name'), number_records)

            context = {
                'paginator': paginator['paginator'],
                'page_objects': paginator['page_objects'],
                'params': urlencode(params),
                'filters_alph': filters_alph,
            }
        else:
            context = {}

        return context

    def split_alph_list(self, a, n):
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))