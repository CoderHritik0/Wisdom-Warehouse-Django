from .notes_views import *
from .auth_views import *
from .profile_views import *

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from ..models import note, note_image


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
