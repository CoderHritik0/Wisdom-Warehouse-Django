from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
# from ..forms import UserRegistrationForm, AuthenticationForm, CustomPasswordResetForm
# Import forms (organized by module)
from ..forms.user_forms import UserRegistrationForm, AuthenticationForm
from ..forms.account_forms import CustomPasswordResetForm
from django.contrib.auth.models import User


def signup(request):
    """Handle user signup."""
    form = UserRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()
        login(request, user)
        messages.success(request, "Signup successful.")
        return redirect("index")
    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    """User login."""
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user:
            login(request, user)
            return redirect("index")
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """Logout user and redirect to homepage."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return render(request, "website/index.html")


def forgot_password(request):
    """Simplified password reset placeholder."""
    form = CustomPasswordResetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        users = User.objects.filter(email=email)
        if users.exists():
            messages.success(
                request, "Password reset instructions have been sent to your email."
            )
            return redirect("login")
        else:
            form.add_error("email", "No user is associated with this email address.")
    return render(request, "registration/forgot_password.html", {"form": form})
