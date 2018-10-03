from . models import AccessRequest
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class AccessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'space_name',
        )
        model = AccessRequest


class AccessListManagerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'space_name',
            'type',
            'access'
        )
        model = AccessRequest

class StatusAccessSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'space_name',
            'access',
        )
        model = AccessRequest

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.groups.add(Group.objects.get(name='clients'))
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')