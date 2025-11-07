from django import forms
from ..models import note, note_image
from .base import FormControlMixin


class NoteForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = note
        fields = ['title', 'description', 'tag', 'color', 'is_hidden']
        widgets = {
            'description': forms.Textarea(attrs={'id': 'id_description', 'rows': 5}),
            'color': forms.TextInput(attrs={'type': 'color'}),
            'is_hidden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['is_hidden'].widget.attrs['data-note-id'] = str(self.instance.pk)


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class NoteImageForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True, 'class': 'form-control', 'type': 'file'}),
        required=False,
    )

    class Meta:
        model = note_image
        fields = ['image']
