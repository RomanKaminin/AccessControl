from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.contrib.auth.views import auth_login
from django.contrib.auth import authenticate, login


class AjaxFormMixin(object):

    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            response_data = {"form": form.errors }
            return JsonResponse(response_data, status=400)
        else:
            return response

    def form_valid(self, form):
        validated_data = form.clean()
        user = get_user_model().objects.create(
          username=validated_data['username'],
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

        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            response_data = {"form": 'ok'}
            return JsonResponse(response_data, status=200)
        else:
            return response