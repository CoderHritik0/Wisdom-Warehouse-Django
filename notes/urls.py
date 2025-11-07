from django.urls import path
from . import views

# app_name='notes'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_or_edit_note, name='create_note'),
    path('edit/<int:note_id>/', views.create_or_edit_note, name='edit_note'),
    path('hidden/edit/<int:note_id>/', views.create_or_edit_note, name='hidden_edit_note'),
    path('delete_image/<int:image_id>/', views.delete_note_image, name='delete_note_image'),
    path('<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('hidden/', views.show_hidden_notes, name='hidden_notes'),
    path('set_pin/', views.index, name='set_pin'),
]
