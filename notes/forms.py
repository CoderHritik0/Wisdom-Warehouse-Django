from django import forms
from .models import note, note_image, Profile
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class NoteForm(forms.ModelForm):
    class Meta:
        model = note
        fields = ['title', 'description', 'tag', 'color', 'is_hidden']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter note title'}),
            'description': forms.Textarea(attrs={'id':'id_description', 'name':'description', 'class': 'form-control', 'placeholder': 'Enter note description', 'rows': 5}),
            'tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter note tag'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'is_hidden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ Add data-note-id dynamically if instance exists
        if self.instance and self.instance.pk:
            self.fields['is_hidden'].widget.attrs['data-note-id'] = str(self.instance.pk)

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class NoteImageForm(forms.ModelForm):
    class Meta:
        model = note_image
        fields = ['image']
    images = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True,'class': 'form-control', 'type': 'file'}),
        required=False,
    )

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username',
            'id': 'floatingUsername'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email',
            'id': 'floatingEmail'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'id': 'floatingPassword1'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'id': 'floatingPassword2'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
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
    pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Note PIN'}),
        max_length=6,
        min_length=6,
        required=True,
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control btn btn-outline-secondary w-50'}),
        }

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        max_length=30,
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        max_length=30,
        required=False,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        required=False,
    )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
    widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your registered email',
        'id': 'floatingEmail'
    })
    )
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
        email_message.send()

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}),
        required=True,
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        required=True,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        required=True,
    )

class PinResetForm(forms.Form):
    current_pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm old 6 digit PIN'}),
        max_length=6,
        min_length=6,
        required=True,
    )
    new_pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new 6 digit PIN'}),
        max_length=6,
        min_length=6,
        required=True,
    )

class setPinForm(forms.Form):
    pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter 6 digit PIN'}),
        max_length=6,
        min_length=6,
        required=True,
    )

class DeleteAccountForm(forms.Form):
    confirm = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Type DELETE to confirm'}),
        required=True,
    )