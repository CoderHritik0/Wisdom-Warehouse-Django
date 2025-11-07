from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as DjangoAuthForm
from django.contrib.auth.models import User
from .base import FormControlMixin


class UserRegistrationForm(FormControlMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username', 'id': 'floatingUsername'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email', 'id': 'floatingEmail'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter password', 'id': 'floatingPassword1'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'id': 'floatingPassword2'}),
        }


class AuthenticationForm(DjangoAuthForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username',
            'id': 'floatingUsername'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password',
            'id': 'floatingPassword'
        })
