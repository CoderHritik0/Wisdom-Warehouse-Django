from django.contrib import messages
from .models import Profile, note, note_image
from .forms import NoteForm, NoteImageForm, UserRegistrationForm, AuthenticationForm, PinSetForm, PinCheckForm, ProfileForm, CustomPasswordResetForm, PasswordChangeForm, PinResetForm, setPinForm, DeleteAccountForm
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.
@login_required
def index(request):
    """Display all non-hidden notes, or handle PIN verification to show hidden notes."""
    hidden = False
    form = PinCheckForm(request.POST or None)
    profile = request.user.profile
    user = request.user

    tag = request.GET.get('tag')
    color = request.GET.get('color')
    search = request.GET.get('search')

    # ✅ Handle PIN form submission
    if request.method == "POST" and form.is_valid():
        input_pin = form.cleaned_data.get('pin')

        if profile and check_password(input_pin, profile.pin):
            return redirect('hidden_notes')
        else:
            form.add_error('pin', 'Incorrect PIN. Please try again.')

    # ✅ Fetch visible notes
    notes = (
        note.objects.filter(user=user, is_deleted=False, is_hidden=hidden)
        .prefetch_related('note_image_set')  # Optimized image fetch
        .order_by('-updated_at')
    )

    notes, all_tags, all_colors = filter_notes(tag, color, user, notes, hidden, search)
    # ✅ Preprocess note images (common logic)
    process_note_images(notes)

    return render(
        request,
        'notes/index.html',
        {'notes': notes, 'all_tags': all_tags, 'all_colors': all_colors, 'selected_tag': tag or "all", 'selected_color': color or "all", 'PinCheckForm': form, 'hidden': hidden, 'profile': profile}
    )

@login_required
def show_hidden_notes(request):
    hidden = True
    profile = request.user.profile
    user = request.user
    tag = request.GET.get('tag')
    color = request.GET.get('color')
    search = request.GET.get('search')

    notes = (
        note.objects.filter(user=request.user, is_deleted=False, is_hidden=hidden)
        .prefetch_related('note_image_set')
        .order_by('-updated_at')
    )
    notes, all_tags, all_colors = filter_notes(tag, color, user, notes, hidden, search)
    process_note_images(notes)
    return render(request, 'notes/index.html', {'notes': notes, 'all_tags': all_tags, 'all_colors': all_colors, 'selected_tag': tag or "all", 'selected_color': color or "all", 'hidden': hidden})

def filter_notes(tag, color, user, notes=None, hidden=False, search=None):
    """Filter notes by tag, color, and optional search query."""

    # --- Apply tag and color filters ---
    if tag and tag != "all":
        notes = notes.filter(tag__iexact=tag)
    if color and color != "all":
        notes = notes.filter(color__iexact=color)

    # --- Apply search filter ---
    if search and search.strip():
        notes = notes.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(tag__icontains=search)
        )

    # --- Build Dropdown Lists (context-aware) ---
    if tag and tag != "all":
        all_colors = (
            note.objects
            .filter(user=user, is_hidden=hidden, tag__iexact=tag)
            .exclude(color__isnull=True)
            .exclude(color__exact="")
            .values_list('color', flat=True)
            .distinct()
        )
    else:
        all_colors = (
            note.objects
            .filter(user=user, is_hidden=hidden)
            .exclude(color__isnull=True)
            .exclude(color__exact="")
            .values_list('color', flat=True)
            .distinct()
        )

    if color and color != "all":
        all_tags = (
            note.objects
            .filter(user=user, is_hidden=hidden, color__iexact=color)
            .exclude(tag__isnull=True)
            .exclude(tag__exact="")
            .values_list('tag', flat=True)
            .distinct()
        )
    else:
        all_tags = (
            note.objects
            .filter(user=user, is_hidden=hidden)
            .exclude(tag__isnull=True)
            .exclude(tag__exact="")
            .values_list('tag', flat=True)
            .distinct()
        )

    return notes, all_tags, all_colors

@require_POST
@login_required
def delete_note_image(request, image_id):
    if request.method == 'POST':
        try:
            image = get_object_or_404(note_image, image_id=image_id)
            image.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def create_or_edit_note(request, note_id=None):
    # If note_id exists → edit, else create new
    note_instance = get_object_or_404(note, pk=note_id, user=request.user) if note_id else None

    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES, instance=note_instance)
        image_form = NoteImageForm(request.POST, request.FILES)

        if form.is_valid():
            saved_note = form.save(commit=False)
            saved_note.user = request.user
            saved_note.save()

            # If new images were uploaded, add them
            for img in request.FILES.getlist('images'):
                note_image.objects.create(note=saved_note, image=img)

            return redirect('index')  # Always redirect after POST ✅
        else:
            print(form.errors)
    else:
        form = NoteForm(instance=note_instance)
        image_form = NoteImageForm()

    return render(request, "notes/create_note.html", {
        "form": form,
        "image_form": image_form,
        "note": note_instance,
        "pin_form": PinSetForm(request)
    })


@login_required
def delete_note(request, note_id):
    note_instance = get_object_or_404(note, pk=note_id, user=request.user)
    note_instance.is_deleted = True
    note_instance.save()
    return redirect('index')

def signup(request):
    # print("signup view")
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('index')  # Redirect to index or login page after successful signup
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, "registration/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # or your notes list page
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return render(request, 'website/index.html')

def setPin(request):
    if request.method == "POST":
        if request.user.profile:
            profile = request.user.profile
            profile.pin = make_password(request.POST.get('pin'))
            profile.save()
    return JsonResponse({'status': 'PIN set successfully'}, status=200)

# ✅ Common helper function
def process_note_images(notes):
    """Attach scaled image data to each note (DRY)."""
    FIXED_WIDTH = 403
    for n in notes:
        images = list(n.note_image_set.all())
        scaled_heights = [
            (img.image.height / img.image.width) * FIXED_WIDTH
            for img in images if img.image and img.image.width and img.image.height
        ]
        n.max_height = max(scaled_heights, default=0)
        for img in images:
            if img.image and img.image.width and img.image.height:
                h = (img.image.height / img.image.width) * FIXED_WIDTH
                img.scaled_height = int(h)
                img.half_diff = int((n.max_height - h) / 2)
            else:
                img.scaled_height, img.half_diff = 0, 0
        n.processed_images = images

@login_required
def profile(request):
    user = request.user
    profile = user.profile  # shortcut

    if request.method == "POST":
        # Detect which form was submitted
        if "update_profile" in request.POST:
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            password_change_form = PasswordChangeForm()  # keep empty for rendering
            pin_reset_form = PinResetForm()  # keep empty for rendering
            pin_set_form = setPinForm()  # keep empty for rendering
            delete_account_form = DeleteAccountForm()  # keep empty for rendering

            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                pin = form.cleaned_data.get('pin')
                profile_picture = form.cleaned_data.get('profile_picture')

                if pin:
                    profile.pin = make_password(pin)
                if profile_picture:
                    profile.profile_picture = profile_picture
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name

                user.save()
                profile.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("profile")
            else:
                messages.error(request, "Fill in the profile form correctly.")

        elif "change_password" in request.POST:
            password_change_form = PasswordChangeForm(request.POST)
            form = ProfileForm(instance=profile)
            pin_reset_form = PinResetForm()  # keep empty for rendering
            pin_set_form = setPinForm()  # keep empty for rendering
            delete_account_form = DeleteAccountForm()  # keep empty for rendering

            if password_change_form.is_valid():
                current_password = password_change_form.cleaned_data.get('current_password')
                new_password = password_change_form.cleaned_data.get('new_password')
                confirm_password = password_change_form.cleaned_data.get('confirm_password')

                if not user.check_password(current_password):
                    password_change_form.add_error('current_password', 'Current password is incorrect.')
                    messages.error(request, "Fill in the password form correctly.")
                elif new_password != confirm_password:
                    password_change_form.add_error('confirm_password', 'New password and confirmation do not match.')
                    messages.error(request, "Fill in the password form correctly.")
                else:
                    user.set_password(new_password)
                    user.save()
                    return redirect('login')
            else:
                messages.error(request, "Fill in the password form correctly.")
        elif "reset_pin" in request.POST:
            pin_reset_form = PinResetForm(request.POST)
            form = ProfileForm(instance=profile)
            password_change_form = PasswordChangeForm()
            pin_set_form = setPinForm()
            delete_account_form = DeleteAccountForm()

            if pin_reset_form.is_valid():
                new_pin = pin_reset_form.cleaned_data.get('new_pin')
                current_pin = pin_reset_form.cleaned_data.get('current_pin')
                if profile.pin and not check_password(current_pin, profile.pin):
                    pin_reset_form.add_error('current_pin', 'Current PIN is incorrect.')
                    messages.error(request, "Please enter the correct current PIN.")
                    return render(
                        request,
                        "registration/profile.html",
                        {
                            "form": form,
                            "user": user,
                            "profile": profile,
                            "password_change_form": password_change_form,
                            "pin_reset_form": pin_reset_form
                        }
                    )
                profile.pin = make_password(new_pin)
                profile.save()
                messages.success(request, "PIN reset successfully.")
                return redirect("profile")
            else:
                messages.error(request, "Please enter the correct current PIN.")
        elif "pin_set_form" in request.POST:
            pin_set_form = setPinForm(request.POST)
            form = ProfileForm(instance=profile)
            password_change_form = PasswordChangeForm()
            pin_reset_form = PinResetForm()
            delete_account_form = DeleteAccountForm()

            if pin_set_form.is_valid():
                new_pin = pin_set_form.cleaned_data.get('pin')
                profile.pin = make_password(new_pin)
                profile.save()
                messages.success(request, "PIN set successfully.")
                return redirect("profile")
            else:
                print(pin_set_form.errors)
                messages.error(request, "Fill in the PIN set form correctly.")
        elif "delete_account" in request.POST:
            delete_account_form = DeleteAccountForm(request.POST)
            form = ProfileForm(instance=profile)
            password_change_form = PasswordChangeForm()
            pin_reset_form = PinResetForm()
            pin_set_form = setPinForm()

            if delete_account_form.is_valid():
                confirmation = delete_account_form.cleaned_data.get('confirm')
                if confirmation == "DELETE":
                    user.delete()
                    messages.success(request, "Account deleted successfully.")
                    return redirect('signup')
                else:
                    delete_account_form.add_error('confirm', 'You must type DELETE to confirm account deletion.')
                    messages.error(request, "Please fill in the delete account field correctly.")
    else:
        form = ProfileForm(instance=profile)
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        password_change_form = PasswordChangeForm()
        pin_reset_form = PinResetForm()
        pin_set_form = setPinForm()
        delete_account_form = DeleteAccountForm()

    return render(
        request,
        "registration/profile.html",
        {
            "form": form,
            "user": user,
            "profile": profile,
            "password_change_form": password_change_form,
            "pin_reset_form": pin_reset_form,
            "pin_set_form": pin_set_form,
            "delete_account_form": delete_account_form
        }
    )

def forgot_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    # Here you would typically send an email with a reset link
                    pass
                messages.success(request, "Password reset instructions have been sent to your email.")
                return redirect('login')
            else:
                form.add_error('email', 'No user is associated with this email address.')
    return render(request, "registration/forgot_password.html", {"form": CustomPasswordResetForm()})