from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # ✅ fixed

from notes.forms import CustomPasswordResetForm
from notesApp.forms import CustomSetPasswordForm
from . import views
from notes import views as notes_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('features/', views.features, name='features'),
    path('notes/', include('notes.urls')),
    path('profile/', notes_views.profile, name='profile'),

    # Password reset URLs
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            form_class=CustomPasswordResetForm,
            html_email_template_name="registration/password_reset_email.html",  # ✅
            subject_template_name='registration/password_reset_email_subject.txt',

        ),
        name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            form_class=CustomSetPasswordForm
        ),
        name="password_reset_confirm"
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
