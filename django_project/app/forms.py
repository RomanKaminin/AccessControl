from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from app.models import AccessRequest
from django.utils.translation import ugettext_lazy as _

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = _("Username"),
        max_length = 32,
        widget=forms.TextInput(
            attrs={'placeholder': _("Username")}
        )
    )
    first_name = forms.CharField(
        required = True,
        label = 'First Name',
        max_length = 32,
        widget=forms.TextInput(
            attrs={'placeholder': _("First Name")}
        )
    )
    last_name = forms.CharField(
        required = True,
        label = 'Last Name',
        max_length = 32,
        widget=forms.TextInput(
            attrs={'placeholder': _("Last Name")}
        )
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
        widget=forms.TextInput(
            attrs={'placeholder': _("Email")}
        )
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput(
            attrs={'placeholder': _("Password")}
        )
    )
    def clean(self):
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')

        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username,first_name=first_name).exists():
            raise forms.ValidationError(
                _("Sorry, user with that username and first name already exist.")
            )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Sorry, that email already exist."))
        return self.cleaned_data

class UserLoginForm(forms.Form):
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
        widget=forms.TextInput(
            attrs={'placeholder': _("Email")}
        )
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget=forms.PasswordInput(
            attrs={'placeholder': _("Password")}
        )
    )
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError(_("Incorrect password."))
            elif not user.is_active:
                raise forms.ValidationError(_("User with this e-mail is blocked."))
        except User.DoesNotExist:
            raise forms.ValidationError(_("User with this e-mail does not exist."))
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user_obj = User.objects.get(email=email)
        user = authenticate(username=user_obj.username, password=password)
        return user


class CreateAccessForm(forms.ModelForm):
    class Meta:
        model = AccessRequest
        fields = ['space_name','email']

    space_name = forms.CharField(
        required = True,
        label = _("Purpose of request"),
        max_length = 32,
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )

    def clean(self):
        return self.cleaned_data

class EditAccessForm(forms.ModelForm):
    class Meta:
        model = AccessRequest
        fields = ['access', 'username', 'space_name']

    access = forms.CharField(
        required = True,
        label = _("Purpose of request"),#Цель запроса
        max_length = 32,
    )
    username = forms.CharField(
        required = True,
        label = _("Username"),
        max_length = 32,
    )
    space_name = forms.CharField(
        required = True,
        label = _("Purpose of request"),
        max_length = 32,
    )

    def clean(self):
        return self.cleaned_data

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
