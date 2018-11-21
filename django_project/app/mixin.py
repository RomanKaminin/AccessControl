from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.contrib.auth.views import auth_login
from django.contrib.auth import authenticate, login


class AjaxRegistrationMixin(object):

    def form_invalid(self, form):
        if self.request.is_ajax():
            response_data = {"form": form.errors }
            return JsonResponse(response_data, status=400)
        else:
            return super(AjaxRegistrationMixin, self).form_invalid(form)

    def form_valid(self, form):
        validated_data = form.clean()
        user = get_user_model().objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.groups.add(Group.objects.get(name='clients'))
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        user_auth = authenticate(username = validated_data['username'],
                               password = validated_data['password']
                               )
        login(self.request, user_auth)
        auth_login(self.request, user_auth)

        if self.request.is_ajax():
            response_data = {"form": 'ok'}
            return JsonResponse(response_data, status=200)
        else:
            return super(AjaxRegistrationMixin, self).form_valid(form)

class AjaxLoginMixin(object):

    def form_invalid(self, form):
        if self.request.is_ajax():
            response_data = {"form": form.errors }
            return JsonResponse(response_data, status=400)
        else:
            return super(AjaxLoginMixin, self).form_invalid(form)

    def form_valid(self, form):
        user = form.login(self.request)
        login(self.request, user)
        if self.request.is_ajax():
            response_data = {"form": 'ok'}
            return JsonResponse(response_data, status=200)
        else:
            return super(AjaxLoginMixin, self).form_valid(form)