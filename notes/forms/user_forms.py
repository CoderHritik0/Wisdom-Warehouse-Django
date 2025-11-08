from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as DjangoAuthForm
from django.contrib.auth.models import User
from .base import FormControlMixin


class UserRegistrationForm(FormControlMixin, UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": " ",  # 👈 keep a space for Bootstrap floating
                "id": "id_password1",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": " ",
                "id": "id_password2",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Enter username",
                    "id": "floatingUsername",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter email",
                    "id": "floatingEmail",
                    "class": "form-control",
                }
            ),
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
