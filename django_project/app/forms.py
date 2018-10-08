from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
        widget=forms.TextInput(
            attrs={'placeholder': 'Username'}
        )
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
        widget=forms.TextInput(
            attrs={'placeholder': 'Email'}
        )
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        )
    )
    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Sorry, that login already exist.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Sorry, that email already exist.")
        return self.cleaned_data

class UserLoginForm(forms.Form):
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
        widget=forms.TextInput(
            attrs={'placeholder': 'Email'}
        )
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        )
    )
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError(u'Incorrect password.')
            elif not user.is_active:
                raise forms.ValidationError(u'User with this e-mail is blocked.')
        except User.DoesNotExist:
            raise forms.ValidationError(u'User with this e-mail does not exist.')
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user_obj = User.objects.get(email=email)
        user = authenticate(username=user_obj.username, password=password)
        return user