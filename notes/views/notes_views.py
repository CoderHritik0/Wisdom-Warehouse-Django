from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from notes.views.profile_views import profile
from ..models import note, note_image
# from ..forms import NoteForm, NoteImageForm, PinSetForm, PinCheckForm
# Import forms (organized by module)
from ..forms.note_forms import NoteForm, NoteImageForm
from ..forms.profile_forms import PinSetForm, PinCheckForm
from .utils import filter_notes, process_note_images, delete_image, handle_verify_pin, handle_pin_set


@login_required
def index(request):
    """Display visible notes and handle PIN verification."""

    user = request.user
    profile = user.profile
    hidden = False
    tag, color, search = (
        request.GET.get("tag"),
        request.GET.get("color"),
        request.GET.get("search"),
    )

    form = PinCheckForm(request.POST or None)
    pin_set_form = PinSetForm()

    if request.method == "POST" and "pin_set_form" in request.POST:
        if handle_pin_set(request, profile):
            return redirect("index")

    if request.method == "POST" and "verify_pin" in request.POST:
        if handle_verify_pin(request, profile):
            return redirect("hidden_notes")
    
    # Notes
    notes = (
        note.objects.filter(user=user, is_deleted=False, is_hidden=hidden)
        .prefetch_related("note_image_set")
        .order_by("-updated_at")
    )
    notes, all_tags, all_colors = filter_notes(tag, color, user, notes, hidden, search)
    process_note_images(notes)

    return render(
        request,
        "notes/index.html",
        {
            "notes": notes,
            "all_tags": all_tags,
            "all_colors": all_colors,
            "selected_tag": tag or "all",
            "selected_color": color or "all",
            "verify_pin_form": form,
            "pin_set_form": pin_set_form,
            "hidden": hidden,
            "profile": profile,
        },
    )


@login_required
def show_hidden_notes(request):
    """Display user's hidden notes (after correct PIN verification)."""
    user = request.user
    hidden = True
    tag, color, search = (
        request.GET.get("tag"),
        request.GET.get("color"),
        request.GET.get("search"),
    )

    notes = (
        note.objects.filter(user=user, is_deleted=False, is_hidden=hidden)
        .prefetch_related("note_image_set")
        .order_by("-updated_at")
    )
    notes, all_tags, all_colors = filter_notes(tag, color, user, notes, hidden, search)
    process_note_images(notes)

    return render(
        request,
        "notes/index.html",
        {
            "notes": notes,
            "all_tags": all_tags,
            "all_colors": all_colors,
            "selected_tag": tag or "all",
            "selected_color": color or "all",
            "hidden": hidden,
        },
    )


@login_required
def create_or_edit_note(request, note_id=None):
    """Create or edit a note with optional image uploads."""
    note_instance = (
        get_object_or_404(note, pk=note_id, user=request.user) if note_id else None
    )
    profile = request.user.profile
    verify_pin_form = PinCheckForm(request.POST or None)

    if request.method == "POST":
        if request.method == "POST" and "verify_pin" in request.POST:
            if handle_verify_pin(request, profile):
                return redirect("hidden_notes")
    
        form = NoteForm(request.POST, request.FILES, instance=note_instance)
        if form.is_valid():
            saved_note = form.save(commit=False)
            saved_note.user = request.user
            saved_note.save()

            for img in request.FILES.getlist("images"):
                note_image.objects.create(note=saved_note, image=img)

            return redirect("index")
        else:
            print(form.errors)
    else:
        form = NoteForm(instance=note_instance)

    return render(
        request,
        "notes/create_note.html",
        {
            "form": form,
            "image_form": NoteImageForm(),
            "note": note_instance,
            "pin_form": PinSetForm(request),
            "verify_pin_form": verify_pin_form,
        },
    )


@login_required
@require_POST
def delete_note_image(request, image_id):
    """Delete a note image via AJAX."""
    return delete_image(request, image_id)


@login_required
def delete_note(request, note_id):
    """Soft delete a note."""
    note_instance = get_object_or_404(note, pk=note_id, user=request.user)
    note_instance.is_deleted = True
    note_instance.save()
    return redirect("index")
