from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse

from ..models import note, note_image
from ..forms.profile_forms import PinCheckForm, PinSetForm



def filter_notes(tag, color, user, notes=None, hidden=False, search=None):
    """Filter notes by tag, color, and search query. Return filtered notes + tag/color lists."""
    if tag and tag != "all":
        notes = notes.filter(tag__iexact=tag)
    if color and color != "all":
        notes = notes.filter(color__iexact=color)
    if search and search.strip():
        notes = notes.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(tag__icontains=search)
        )

    # Dynamic dropdowns
    all_colors = (
        note.objects.filter(
            user=user,
            is_hidden=hidden,
            **({"tag__iexact": tag} if tag and tag != "all" else {}),
        )
        .exclude(color__isnull=True)
        .exclude(color__exact="")
        .values_list("color", flat=True)
        .distinct()
    )
    all_tags = (
        note.objects.filter(
            user=user,
            is_hidden=hidden,
            **({"color__iexact": color} if color and color != "all" else {}),
        )
        .exclude(tag__isnull=True)
        .exclude(tag__exact="")
        .values_list("tag", flat=True)
        .distinct()
    )
    return notes, all_tags, all_colors


def process_note_images(notes):
    """Precompute scaled image heights for uniform display."""
    FIXED_WIDTH = 403
    for n in notes:
        images = list(n.note_image_set.all())
        scaled_heights = [
            (img.image.height / img.image.width) * FIXED_WIDTH
            for img in images
            if img.image and img.image.width and img.image.height
        ]
        n.max_height = max(scaled_heights, default=0)
        for img in images:
            if img.image and img.image.width and img.image.height:
                h = (img.image.height / img.image.width) * FIXED_WIDTH
                img.scaled_height = int(h)
                img.half_diff = int((n.max_height - h) / 2)
            else:
                img.scaled_height = img.half_diff = 0
        n.processed_images = images


def delete_image(request, image_id):
    """Generic note image delete handler (used by AJAX)."""
    try:
        image = get_object_or_404(note_image, image_id=image_id)
        image.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
    

def handle_verify_pin(request, profile):
    """Handle verifying PIN to access hidden notes."""
    form = PinCheckForm(request.POST)
    if form.is_valid():
        if check_password(form.cleaned_data['pin'], profile.pin):
            messages.success(request, "PIN verified successfully.")
            return redirect('hidden_notes')
        messages.error(request, "Please enter the correct PIN to view hidden notes.")
    else:
        messages.error(request, "PIN should be 6 digits.")
    return None


def handle_pin_set(request, profile):
    """Handle setting new PIN for the first time."""
    form = PinSetForm(request.POST)
    if form.is_valid():
        profile.pin = make_password(form.cleaned_data['pin'])
        profile.save()
        messages.success(request, "PIN set successfully.")
        return redirect("profile")

    messages.error(request, "Fill in the PIN set form correctly.")
    return None
