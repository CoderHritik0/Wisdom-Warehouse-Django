from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

# from ..forms import (
#     ProfileForm, PasswordChangeForm, PinResetForm, SetPinForm, DeleteAccountForm, PinCheckForm
# )
# Import forms (organized by module)
from ..forms.profile_forms import PinSetForm, ProfileForm, PinCheckForm, PinResetForm
from ..forms.account_forms import PasswordChangeForm, DeleteAccountForm
from .utils import handle_verify_pin, handle_pin_set

# ======================================================
# 🧩 Helper Handlers — Single Responsibility Each
# ======================================================

def handle_profile_update(request, user, profile):
    """Handle updating basic profile info (name, picture, pin)."""
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        user.first_name = form.cleaned_data.get('first_name', user.first_name)
        user.last_name = form.cleaned_data.get('last_name', user.last_name)

        pin = form.cleaned_data.get('pin')
        if pin:
            profile.pin = make_password(pin)

        profile_picture = form.cleaned_data.get('profile_picture')
        if profile_picture:
            profile.profile_picture = profile_picture

        user.save()
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    messages.error(request, "Fill in the profile form correctly.")
    return None


def handle_password_change(request, user):
    """Handle password change form."""
    form = PasswordChangeForm(request.POST)
    if form.is_valid():
        current = form.cleaned_data['current_password']
        new = form.cleaned_data['new_password']
        confirm = form.cleaned_data['confirm_password']

        if not user.check_password(current):
            messages.error(request, "Current password is incorrect.")
            form.add_error('current_password', 'Current password is incorrect.')
        elif new != confirm:
            messages.error(request, "New passwords do not match.")
            form.add_error('confirm_password', 'Passwords do not match.')
        else:
            user.set_password(new)
            user.save()
            messages.success(request, "Password changed successfully. Please log in again.")
            return redirect('login')
    
    return None


def handle_pin_reset(request, profile):
    """Handle reset PIN form."""
    form = PinResetForm(request.POST)
    if form.is_valid():
        current_pin = form.cleaned_data['current_pin']
        new_pin = form.cleaned_data['new_pin']

        if profile.pin and not check_password(current_pin, profile.pin):
            messages.error(request, "Current PIN is incorrect.")
            form.add_error('current_pin', 'Current PIN is incorrect.')
            return None
        else:
            profile.pin = make_password(new_pin)
            profile.save()
            messages.success(request, "PIN reset successfully.")
            return redirect("profile")

    messages.error(request, "Please enter the correct current PIN.")
    return None


def handle_delete_account(request, user):
    """Handle account deletion with confirmation."""
    form = DeleteAccountForm(request.POST)
    if form.is_valid():
        confirmation = form.cleaned_data['confirm']
        if confirmation == "DELETE":
            user.delete()
            messages.success(request, "Account deleted successfully.")
            return redirect('signup')
        else:
            form.add_error('confirm', 'You must type DELETE to confirm account deletion.')

    messages.error(request, "Please fill in the delete account field correctly.")
    return None


# ======================================================
# 👤 Profile Main View
# ======================================================

@login_required
def profile(request):
    """
    Handle user profile management:
    - Update profile info
    - Change password
    - Reset or set PIN
    - Verify PIN to view hidden notes
    - Delete account
    """

    user = request.user
    profile = user.profile

    # Initialize all forms (for rendering)
    forms = {
        "form": ProfileForm(instance=profile),
        "password_change_form": PasswordChangeForm(),
        "pin_reset_form": PinResetForm(),
        "pin_set_form": PinSetForm(),
        "delete_account_form": DeleteAccountForm(),
        "verify_pin_form": PinCheckForm(),
    }

    # Pre-fill names for convenience
    forms["form"].fields['first_name'].initial = user.first_name
    forms["form"].fields['last_name'].initial = user.last_name

    if request.method == "POST":
        # ✅ Dispatch table for form handling
        actions = {
            "update_profile": lambda: handle_profile_update(request, user, profile),
            "change_password": lambda: handle_password_change(request, user),
            "reset_pin": lambda: handle_pin_reset(request, profile),
            "pin_set_form": lambda: handle_pin_set(request, profile),
            "verify_pin": lambda: handle_verify_pin(request, profile),
            "delete_account": lambda: handle_delete_account(request, user),
        }

        # 🔁 Dynamically call the correct handler
        for key, action in actions.items():
            if key in request.POST:
                result = action()
                if result:
                    return result  # redirect or render handled inside handler
                break
        else:
            messages.error(request, "Unrecognized form submission.")

    return render(request, "registration/profile.html", {"user": user, "profile": profile, **forms})
