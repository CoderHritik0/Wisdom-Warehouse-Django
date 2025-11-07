from django import forms

class FormControlMixin:
    """Adds Bootstrap form-control class to all non-checkbox fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-control')


def pin_field(placeholder):
    """Reusable 6-digit masked PIN field."""
    return forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': placeholder}),
        max_length=6,
        min_length=6,
        required=True,
    )
