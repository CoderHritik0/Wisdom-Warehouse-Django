from django.contrib import messages
from django import forms
from ..models import Profile
from .base import FormControlMixin, pin_field


class ProfileForm(FormControlMixin, forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )

    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control btn btn-outline-secondary w-50'}),
        }


class PinSetForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pin']
        widgets = {
            'pin': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter 6 digit PIN', 'id': 'setNotePin'}),
        }

    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        if pin and (not pin.isdigit() or len(pin) != 6):
            raise forms.ValidationError("PIN must be 6 digits.")
        return pin


class PinCheckForm(forms.Form):
    pin = pin_field('Enter Note PIN')


class PinResetForm(forms.Form):
    current_pin = pin_field('Confirm old 6 digit PIN')
    new_pin = pin_field('Enter new 6 digit PIN')

    def clean_new_pin(self):
        pin = self.cleaned_data.get('new_pin')
        if pin and (not pin.isdigit() or len(pin) != 6):
            raise forms.ValidationError("PIN must be 6 digits.")
        return pin


class SetPinForm(forms.Form):
    pin = pin_field('Enter 6 digit PIN')
