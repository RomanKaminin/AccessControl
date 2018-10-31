from rest_framework.views import APIView
from app.models import AccessRequest
from app.serializers import AccessRequestSerializer, AccessListManagerSerializer,  \
    StatusAccessSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.http import Http404
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from app.permissions import HasGroupPermission
from django.contrib.auth import logout

class SendRequest(generics.ListCreateAPIView):
    """
    Отправляет заявку на доступ в помещение.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer

class AllRequests(APIView):
    """
    Выводит все необработанные заявки.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['managers'],
    }
    def get(self, request):
        requests = AccessRequest.objects.filter(access='empty')
        serializer = AccessListManagerSerializer(requests, many=True)
        return Response(serializer.data)

class AccessDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['clients'],
        'PUT': ['managers'],
        'DELETE': ['managers'],
    }

    def get_object(self, pk):
        try:
            return AccessRequest.objects.get(pk=pk)
        except AccessRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Просмотр текущего статуса заявки.
        """
        user = self.get_object(pk)
        user = StatusAccessSerializer(user)
        return Response(user.data)

    def put(self, request, pk, format=None):
        """
        Подтверждение или отказ заявки (может только админ).
        """
        user = self.get_object(pk)
        serializer = StatusAccessSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        """
        Удаление заявки.
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateUserView(CreateAPIView):
    """
    1.Регистрация пользователя с ответом токена.
    """
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key,}, status=status.HTTP_201_CREATED, headers=headers)

class AuthView(APIView):
    """
    1.Проверка аунтификации.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response({'detail': "I suppose you are authenticated"})


class LogoutUser(ListAPIView):
    """
    1.Выход из системы.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def logout(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_online = False
        instance.save()

    def post(self, request, *args, **kwargs):
        self.logout()
        return Response()

    def get(self, request, *args, **kwargs):
        self.logout()
        return logout(request)